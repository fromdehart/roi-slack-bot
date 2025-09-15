#!/usr/bin/env python3
"""
Safe executor for LLM-generated graph code
Runs in a Docker container with restricted permissions
"""

import os
import sys
import json
import tempfile
import logging
from graph_generator import get_graph_code_from_llm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_execute_graph_code(python_code, output_path):
    """
    Safely execute Python code with restricted environment
    """
    try:
        # Create a very restricted execution environment
        safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'min': min,
                'max': max,
                'sum': sum,
                'abs': abs,
                'round': round,
                'int': int,
                'float': float,
                'str': str,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'bool': bool,
                'type': type,
                'isinstance': isinstance,
                'hasattr': hasattr,
                'getattr': getattr,
                'setattr': setattr,
                'Exception': Exception,
                'ValueError': ValueError,
                'TypeError': TypeError,
            }
        }
        
        # Import only safe modules
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        
        safe_globals.update({
            'matplotlib': matplotlib,
            'plt': plt,
            'pandas': pd,
            'pd': pd,
            'numpy': np,
            'np': np,
        })
        
        # Execute the code
        exec(python_code, safe_globals)
        
        # Verify output file was created
        if not os.path.exists('output.png'):
            raise Exception("Code did not create output.png file")
        
        # Move the file to the specified output path
        os.rename('output.png', output_path)
        
        return True
        
    except Exception as e:
        logger.error(f"Error executing graph code: {str(e)}")
        return False

def main():
    """Main execution function for containerized environment"""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        user_request = input_data.get('user_request')
        
        if not user_request:
            raise ValueError("No user_request provided")
        
        logger.info(f"Processing request: {user_request}")
        
        # Get Python code from LLM
        python_code = get_graph_code_from_llm(user_request)
        logger.info("Generated Python code from LLM")
        
        # Create output file path
        output_path = '/tmp/graph_output.png'
        
        # Execute the code safely
        success = safe_execute_graph_code(python_code, output_path)
        
        if success:
            # Return success response
            response = {
                'success': True,
                'output_path': output_path,
                'message': 'Graph generated successfully'
            }
        else:
            response = {
                'success': False,
                'error': 'Failed to generate graph'
            }
        
        print(json.dumps(response))
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        error_response = {
            'success': False,
            'error': str(e)
        }
        print(json.dumps(error_response))
        sys.exit(1)

if __name__ == "__main__":
    main()
