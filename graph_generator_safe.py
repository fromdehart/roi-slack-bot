#!/usr/bin/env python3
"""
Safe graph generator using Docker containers
"""

import os
import json
import subprocess
import tempfile
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class SafeGraphGenerator:
    def __init__(self, use_docker=True):
        self.use_docker = use_docker
        self.docker_image = "roi-graph-generator"
        
    def generate_roi_graph(self, user_request):
        """
        Generate an ROI graph using containerized execution
        Returns path to generated image file
        """
        logger.info(f"Generating graph for request: {user_request}")
        
        if self.use_docker:
            return self._generate_with_docker(user_request)
        else:
            # Fallback to local execution (less safe)
            from graph_generator import generate_roi_graph as local_generate
            return local_generate(user_request)
    
    def _generate_with_docker(self, user_request):
        """Generate graph using Docker container"""
        try:
            # Create temporary output file
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            # Prepare input data
            input_data = {
                'user_request': user_request
            }
            
            # Run Docker container
            cmd = [
                'docker', 'run',
                '--rm',  # Remove container after execution
                '--network=none',  # No network access
                '--memory=512m',  # Limit memory to 512MB
                '--cpus=1',  # Limit to 1 CPU core
                '--user=1000:1000',  # Run as non-root user
                '--read-only',  # Read-only filesystem
                '--tmpfs=/tmp:rw,size=100m',  # Temporary writable space
                '-v', f'{os.path.dirname(temp_path)}:/output:rw',  # Mount output directory
                self.docker_image,
                'python3', 'safe_executor.py'
            ]
            
            logger.info(f"Running Docker command: {' '.join(cmd)}")
            
            # Execute with timeout
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(
                input=json.dumps(input_data),
                timeout=60  # 60 second timeout
            )
            
            if process.returncode != 0:
                logger.error(f"Docker execution failed: {stderr}")
                raise Exception(f"Container execution failed: {stderr}")
            
            # Parse response
            response = json.loads(stdout)
            
            if response.get('success'):
                # The container should have created the file at the mounted location
                container_output_path = response.get('output_path', '/tmp/graph_output.png')
                expected_local_path = os.path.join(os.path.dirname(temp_path), 'graph_output.png')
                
                if os.path.exists(expected_local_path):
                    # Move to our desired temp file location
                    os.rename(expected_local_path, temp_path)
                    logger.info(f"Graph generated successfully: {temp_path}")
                    return temp_path
                else:
                    raise Exception("Container did not create output file")
            else:
                raise Exception(response.get('error', 'Unknown container error'))
                
        except subprocess.TimeoutExpired:
            logger.error("Docker execution timed out")
            raise Exception("Graph generation timed out")
        except Exception as e:
            logger.error(f"Docker execution failed: {str(e)}")
            raise Exception(f"Failed to generate graph: {str(e)}")

def build_docker_image():
    """Build the Docker image for safe execution"""
    try:
        logger.info("Building Docker image for safe graph generation...")
        
        # Build the image
        cmd = ['docker', 'build', '-t', 'roi-graph-generator', '.']
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout
        
        if process.returncode == 0:
            logger.info("Docker image built successfully")
            return True
        else:
            logger.error(f"Docker build failed: {stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("Docker build timed out")
        return False
    except Exception as e:
        logger.error(f"Docker build error: {str(e)}")
        return False

# Convenience function
def generate_roi_graph_safe(user_request):
    """Generate ROI graph with containerized safety"""
    generator = SafeGraphGenerator(use_docker=True)
    return generator.generate_roi_graph(user_request)
