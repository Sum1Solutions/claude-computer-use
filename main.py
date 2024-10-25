from docker_manager import DockerManager

def main():
    try:
        # Initialize the Docker manager
        print("Initializing Docker manager...")
        manager = DockerManager()
        
        # Run the container
        container = manager.run_container()
        
        # Keep the script running until interrupted
        try:
            print("\nContainer is running. Press Ctrl+C to stop...")
            container.wait()
        except KeyboardInterrupt:
            print("\nReceived interrupt signal...")
            manager.stop_container(container)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()