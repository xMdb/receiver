import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import yaml
import shlex

# Functions
def read_data_from_file(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    actions = []
    for action_data in data["requests"]:
        endpoint = action_data["endpoint"]
        action = shlex.split(action_data["action"])
        actions.append((endpoint, action))
    return actions


def run_program(action):
    subprocess.run(["cmd.exe", "/c", "start"] + action)


def send_success_response(self):
    self.send_response(200)
    self.end_headers()
    # send History.back() to browser to close the tab
    self.wfile.write(
        b"<!DOCTYPE html><html><body><h1>Success</h1><script>history.back()</script></body></html>"
    )


def send_not_found_response(self):
    self.send_response(404)
    self.end_headers()
    self.wfile.write(b"404 Not Found")


def send_not_allowed_response(self):
    self.send_response(403)
    self.end_headers()
    self.wfile.write(b"403 Not Allowed")


# Main handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"Received request for {self.path}")
        config_data = read_data_from_file("config.yml")
        if self.client_address[0] == "10.0.10.101":
            for endpoint, action in config_data:
                if self.path == endpoint:
                    run_program(action)
                    send_success_response(self)
                    break
            else:
                send_not_found_response(self)
        else:
            send_not_allowed_response(self)


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logging.info("Starting server...")
server = HTTPServer(("", 1234), RequestHandler)
logging.info("Server started")
server.serve_forever()
