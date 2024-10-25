# Anthropic Computer Use Docker Manager

This Python project provides a secure way to manage Docker containers for Anthropic's Computer Use functionality, with proper environment variable handling and container lifecycle management.

## Prerequisites

- Python 3.8+
- Docker installed and running on your system
- Anthropic API key
- Sufficient permissions to run Docker containers

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd docker-manager
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create your environment configuration:
```bash
cp .env.example .env
```

5. Edit the `.env` file with your configuration:
```ini
ANTHROPIC_API_KEY=your_api_key_here
DOCKER_IMAGE=ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest
HOST_CONFIG_PATH=${HOME}/.anthropic
CONTAINER_CONFIG_PATH=/home/computeruse/.anthropic
```

## Usage

To run the container:
```bash
python main.py
```

The script will:
- Load your configuration from the `.env` file
- Start the Docker container with the specified settings
- Map the required ports (5900, 8501, 6080, 8080)
- Set up the volume mounting for configuration
- Keep running until interrupted with Ctrl+C
- Gracefully stop and remove the container on exit

## Project Structure

```
.
├── requirements.txt       # Project dependencies
├── .env.example          # Example environment configuration
├── docker_manager.py     # Docker container management class
├── main.py              # Main script entry point
└── README.md            # This file
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| ANTHROPIC_API_KEY | Your Anthropic API key | sk-ant-xxxx... |
| DOCKER_IMAGE | The Docker image to use | ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest |
| HOST_CONFIG_PATH | Path to config directory on host | ${HOME}/.anthropic |
| CONTAINER_CONFIG_PATH | Path to config directory in container | /home/computeruse/.anthropic |

## Security Notes

- Never commit your `.env` file containing sensitive information
- Regularly rotate your API keys
- Ensure your Docker daemon is properly secured
- Be cautious when running containers with port mappings

## Error Handling

The script includes comprehensive error handling for:
- Missing environment variables
- Docker daemon connection issues
- Container startup failures
- Graceful shutdown on interruption

## Contributing

Feel free to submit issues and enhancement requests!

## License

[MIT License](LICENSE)

## Additional Resources

- [Anthropic Computer Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/computer-use)
- [Docker Python SDK Documentation](https://docker-py.readthedocs.io/)
- [python-dotenv Documentation](https://pypi.org/project/python-dotenv/)