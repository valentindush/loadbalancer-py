import http.server
import socketserver
import requests
import threading
import time
import logging

backend_servers = [
    {"url": "http://127.0.0.1:8001", "weight": 2},
    {"url": "http://127.0.0.1:8002", "weight": 1}
]

#active connections
active_connections = {server["url"]: 0 for server in backend_servers}

current_server = 0
current_weight = 0

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def health_check():
    while True:
        for i, server in enumerate(backend_servers):
            try:
                response = requests.get(server["url"], timeout=2)
                if response.status_code != 200:
                    logging.warning(f"Server {server['url']} is unhealthy. Removing from pool.")
                    backend_servers.pop(i)
            except requests.RequestException:
                logging.warning(f"Server {server['url']} is unhealthy. Removing from pool.")
                backend_servers.pop(i)
        time.sleep(10)  #every 10 seconds

def get_next_server():
    global current_server, current_weight
    while True:
        server = backend_servers[current_server]
        if current_weight < server["weight"]:
            current_weight += 1
            return server["url"]
        else:
            current_weight = 0
            current_server = (current_server + 1) % len(backend_servers)

def get_least_connections_server():
    return min(active_connections, key=active_connections.get)

class LoadBalancerHandler(http.server.BaseHTTPRequestHandler):
    def forward_request(self, backend):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else None

        try:
            response = requests.request(
                method=self.command,
                url=f"{backend}{self.path}",
                headers=self.headers,
                data=body,
                allow_redirects=False
            )

            self.send_response(response.status_code)
            for header, value in response.headers.items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.content)
        except requests.RequestException as e:
            self.send_error(500, f"Error forwarding request: {e}")

    def do_GET(self):
        backend = get_least_connections_server()
        active_connections[backend] += 1
        logging.info(f"Forwarding request to {backend} (connections: {active_connections[backend]})")
        self.forward_request(backend)
        active_connections[backend] -= 1

    def do_POST(self):
        self.do_GET()

if __name__ == "__main__":
    threading.Thread(target=health_check, daemon=True).start()

    PORT = 8080
    with socketserver.TCPServer(("", PORT), LoadBalancerHandler) as httpd:
        logging.info(f"Load balancer running on port {PORT}...")
        httpd.serve_forever()