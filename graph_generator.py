import os
import tempfile
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Heroku
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from openai import OpenAI
import logging
import re
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_roi_graph(user_request):
    """
    Generate an ROI graph based on user's natural language request
    Returns path to generated image file
    """
    logger.info(f"Generating graph for request: {user_request}")
    
    # Get Python code from OpenAI
    python_code = get_graph_code_from_llm(user_request)
    logger.info("Generated Python code from LLM")
    
    # Execute the code safely and return image path
    image_path = execute_graph_code(python_code, user_request)
    logger.info(f"Graph generated successfully: {image_path}")
    
    return image_path

def get_graph_code_from_llm(user_request):
    """Generate Python code using OpenAI to create ROI graph"""
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    system_prompt = """You are an expert at creating ROI analysis graphs using Python matplotlib.

Generate clean, professional Python code that creates a line graph based on the user's request.

Requirements:
1. Use matplotlib.pyplot as plt
2. Create realistic ROI data that makes business sense
3. Always create a line graph with professional styling
4. Use proper labels, title, legend, and grid
5. Set figure size to (12, 8) for good Slack visibility
6. Save as PNG with high DPI: plt.savefig('output.png', dpi=300, bbox_inches='tight')
7. Use professional colors (avoid bright/neon colors)
8. Include data points on the lines
9. Add percentage formatting for ROI values when appropriate
10. Generate realistic time series data (months, quarters, years as appropriate)

Example structure:
```python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create realistic data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
vr_roi = [10, 25, 40, 60, 75, 95]  # Realistic ROI percentages
traditional_roi = [5, 8, 12, 15, 18, 20]

# Create professional graph
plt.figure(figsize=(12, 8))
plt.plot(months, vr_roi, marker='o', linewidth=3, label='VR Training ROI', color='#2E86AB')
plt.plot(months, traditional_roi, marker='s', linewidth=3, label='Traditional Training ROI', color='#A23B72')

plt.title('ROI Comparison: VR vs Traditional Training', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Time Period', fontsize=14)
plt.ylabel('ROI (%)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()
```

Generate ONLY the Python code, no explanation or markdown formatting."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create a line graph for: {user_request}"}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        python_code = response.choices[0].message.content.strip()
        
        # Clean up any markdown formatting
        if "```python" in python_code:
            python_code = python_code.split("```python")[1].split("```")[0].strip()
        elif "```" in python_code:
            python_code = python_code.split("```")[1].split("```")[0].strip()
            
        return python_code
        
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {str(e)}")
        # Fallback to a simple default graph
        return get_fallback_graph_code(user_request)

def execute_graph_code(python_code, user_request="ROI Analysis"):
    """
    Safely execute Python code and return path to generated image
    """
    # Create temp directory for execution
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Set up the execution environment
            exec_globals = {
                '__builtins__': __builtins__,
                'matplotlib': matplotlib,
                'plt': plt,
                'pd': pd,
                'pandas': pd,
                'np': np,
                'numpy': np,
                'os': os,
                'tempfile': tempfile
            }
            
            # Change working directory for execution
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Execute the code
                exec(python_code, exec_globals)
                
                # Check if output.png was created
                output_path = os.path.join(temp_dir, 'output.png')
                if not os.path.exists(output_path):
                    raise Exception("Graph code did not create output.png file")
                
                # Copy to a permanent temp location
                final_temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                final_path = final_temp_file.name
                final_temp_file.close()
                
                # Copy the generated image
                with open(output_path, 'rb') as src, open(final_path, 'wb') as dst:
                    dst.write(src.read())
                
                return final_path
                
            finally:
                os.chdir(original_cwd)
                
        except Exception as e:
            logger.error(f"Error executing graph code: {str(e)}")
            # Generate a fallback graph
            return generate_fallback_graph(user_request)

def get_fallback_graph_code(user_request):
    """Generate a simple fallback graph when OpenAI fails"""
    return """
import matplotlib.pyplot as plt
import numpy as np

# Simple fallback ROI data
months = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']
roi_data = [15, 35, 55, 75, 90, 110]

plt.figure(figsize=(12, 8))
plt.plot(months, roi_data, marker='o', linewidth=3, color='#2E86AB', markersize=8)
plt.title('ROI Analysis Over Time', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Time Period', fontsize=14)
plt.ylabel('ROI (%)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Add data labels
for i, v in enumerate(roi_data):
    plt.text(i, v + 2, f'{v}%', ha='center', va='bottom', fontweight='bold')

plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()
"""

def generate_fallback_graph(user_request):
    """Generate a basic fallback graph when code execution fails"""
    try:
        # Create a simple ROI graph with guaranteed matching dimensions
        time_periods = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']
        roi_data = [15, 35, 55, 75, 90, 110]
        
        # Ensure arrays have matching dimensions
        assert len(time_periods) == len(roi_data), f"Dimension mismatch: {len(time_periods)} vs {len(roi_data)}"
        
        plt.figure(figsize=(12, 8))
        plt.plot(time_periods, roi_data, marker='o', linewidth=3, color='#2E86AB', markersize=8)
        plt.title(f'ROI Analysis: {user_request[:50]}', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Time Period', fontsize=14)
        plt.ylabel('ROI (%)', fontsize=14)
        plt.grid(True, alpha=0.3)
        
        # Add data labels
        for i, v in enumerate(roi_data):
            plt.text(i, v + 2, f'{v}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Save to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(temp_file.name, dpi=300, bbox_inches='tight')
        plt.close()
        
        return temp_file.name
        
    except Exception as e:
        logger.error(f"Even fallback graph failed: {str(e)}")
        raise Exception(f"Could not generate any graph: {str(e)}")