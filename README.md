# SIMPLE LOAD BALANCER
## Overview

This project is a simple load balancer written in Python. It distributes incoming network traffic across multiple servers to ensure no single server becomes overwhelmed.

## Features

- Round-robin load balancing
- Health checks for backend servers
- Easy to configure and extend

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/loadbalancer.git
    ```
2. Navigate to the project directory:
    ```sh
    cd loadbalancer
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To start the load balancer, run:
```sh
python loadbalancer.py
```

## Configuration

You can configure the load balancer by editing the `config.json` file. Here is an example configuration:
```json
{
  "servers": [
     {"host": "127.0.0.1", "port": 8001},
     {"host": "127.0.0.1", "port": 8002}
  ],
  "health_check_interval": 10
}
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.