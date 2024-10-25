import os
import sys
import docker
import platform
import subprocess
from dotenv import load_dotenv

class DockerManager:
    def __init__(self):
        load_dotenv()
        
        try:
            # Get current Docker context
            try:
                context_result = subprocess.run(
                    ['docker', 'context', 'inspect'], 
                    capture_output=True, 
                    text=True
                )
                if context_result.returncode == 0:
                    print("Using current Docker context")
                    self.client = docker.from_env()
                else:
                    raise Exception("Could not get Docker context")
            except Exception as context_error:
                print(f"Error getting Docker context: {str(context_error)}")
                # Fallback to explicit socket path
                if platform.system().lower() == 'darwin':
                    desktop_socket = os.path.expanduser('~/.docker/run/docker.sock')
                    default_socket = '/var/run/docker.sock'
                    
                    if os.path.exists(desktop_socket):
                        docker_socket = desktop_socket
                    elif os.path.exists(default_socket):
                        docker_socket = default_socket
                    else:
                        raise docker.errors.DockerException(
                            "No valid Docker socket found"
                        )
                    
                    print(f"Using Docker socket at: {docker_socket}")
                    self.client = docker.DockerClient(base_url=f'unix://{docker_socket}')
                else:
                    self.client = docker.from_env()
            
            # Verify connection
            self.client.ping()
            print("Successfully connected to Docker daemon")
            
        except docker.errors.DockerException as e:
            self._handle_docker_init_error(e)
            
        # Get configuration from environment
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.image = os.getenv('DOCKER_IMAGE')
        self.host_config_path = os.path.expandvars(os.getenv('HOST_CONFIG_PATH'))
        self.container_config_path = os.getenv('CONTAINER_CONFIG_PATH')
        
        # Validate required environment variables
        self._validate_config()

    def _validate_config(self):
        """Validate all required environment variables are present."""
        required_vars = ['ANTHROPIC_API_KEY', 'DOCKER_IMAGE', 
                        'HOST_CONFIG_PATH', 'CONTAINER_CONFIG_PATH']
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print("\nMissing required environment variables:")
            for var in missing_vars:
                print(f"- {var}")
            print("\nMake sure you have created a .env file with all required variables.")
            sys.exit(1)

    def run_container(self):
        """Run the Docker container with the specified configuration."""
        try:
            # Pull the image first
            print(f"Pulling image {self.image}...")
            self.client.images.pull(self.image)
            
            print("Starting container...")
            container = self.client.containers.run(
                image=self.image,
                environment={
                    'ANTHROPIC_API_KEY': self.api_key
                },
                volumes={
                    self.host_config_path: {
                        'bind': self.container_config_path,
                        'mode': 'rw'
                    }
                },
                ports={
                    '5900': '5901',  # Changed to use port 5901 instead of 5900
                    '8501': '8501',
                    '6080': '6080',
                    '8080': '8080'
                },
                detach=True,
                tty=True,
                stdin_open=True
            )
            
            print(f"Container started successfully. ID: {container.id}")
            print("\nPorts mapped:")
            print("- VNC: localhost:5901")  # Updated port in message
            print("- Web Interface: localhost:8501")
            print("- Additional ports: 6080, 8080")
            return container
            
        except docker.errors.ImageNotFound:
            print(f"Error: Image '{self.image}' not found.")
            sys.exit(1)
        except docker.errors.DockerException as e:
            print(f"Error running container: {str(e)}")
            raise

    def stop_container(self, container):
        """Stop and remove the specified container."""
        try:
            print("\nStopping container...")
            container.stop()
            print("Removing container...")
            container.remove()
            print("Container stopped and removed successfully.")
        except docker.errors.DockerException as e:
            print(f"Error stopping container: {str(e)}")
            raise

    def _handle_docker_init_error(self, error):
        """Handle Docker initialization errors with helpful messages."""
        os_type = platform.system().lower()
        
        print("Error connecting to Docker daemon. Here's how to fix it:")
        
        if os_type == 'darwin':  # macOS
            socket_paths = ['/var/run/docker.sock', os.path.expanduser('~/.docker/run/docker.sock')]
            print("\nFor macOS users:")
            for socket_path in socket_paths:
                print(f"\nChecking socket at: {socket_path}")
                print(f"1. Check if Docker socket exists:")
                print(f"   ls -l {socket_path}")
                if os.path.exists(socket_path):
                    print(f"   Socket exists: Yes")
                    print("2. Check socket permissions:")
                    print(f"   stat {socket_path}")
                else:
                    print(f"   Socket exists: No")
            
            print("\n3. Verify Docker Desktop is running")
            print("4. Try these commands:")
            print("   docker context ls")
            print("   docker ps")
            print("   docker context inspect desktop-linux")
            print("5. Check Docker context:")
            print("   echo $DOCKER_HOST")
            
        else:
            print("\nFor non-macOS users:")
            print("1. Check if Docker daemon is running:")
            print("   systemctl status docker")
            print("2. Verify Docker permissions:")
            print("   groups | grep docker")
            print("3. Try running:")
            print("   docker ps")
            
        print(f"\nOriginal error: {str(error)}")
        print(f"\nDebug information:")
        print(f"OS: {platform.system()} {platform.release()}")
        print(f"Python version: {sys.version}")
        print(f"Docker socket paths checked:")
        print(f"- /var/run/docker.sock exists: {os.path.exists('/var/run/docker.sock')}")
        print(f"- ~/.docker/run/docker.sock exists: {os.path.exists(os.path.expanduser('~/.docker/run/docker.sock'))}")
        
        try:
            result = subprocess.run(['docker', 'context', 'ls'], 
                                 capture_output=True, text=True)
            print("\nDocker contexts:")
            print(result.stdout)
        except:
            print("Could not get Docker context information")
            
        sys.exit(1)