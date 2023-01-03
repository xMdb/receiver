import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess

# Functions
def run_program(program_path, *args):
    subprocess.run(["cmd.exe", "/c", "start", program_path] + list(args))


def send_success_response(self):
    self.send_response(200)
    self.end_headers()
    # send History.back() to browser to close the tab
    self.wfile.write(b"<!DOCTYPE html><html><body><h1>Success</h1><script>history.back()</script></body></html>")


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
        if self.client_address[0] == "10.0.10.101":
            if self.path == "/ssh/maindns":
                run_program(
                    "wt", "new-tab", "PowerShell", "ssh", "ubuntu@primary.pihole.box"
                )
                send_success_response(self)
            elif self.path == "/ssh/backupdns":
                run_program(
                    "wt", "new-tab", "PowerShell", "ssh", "matt@secondary.pihole.box"
                )
                send_success_response(self)
            elif self.path == "/ssh/nova":
                run_program("wt", "new-tab", "PowerShell", "ssh", "matt@nova.box")
                send_success_response(self)
            elif self.path == "/rdp/torrentbox":
                run_program("mstsc", "/v:torrent.vm.box")
                send_success_response(self)
            elif self.path == "/rdp/winserv":
                run_program("mstsc", "/v:10.1.20.100")
                send_success_response(self)
            elif self.path == "/files/projects":
                run_program("explorer", "'D:\Files\Actual Files\projects'")
                send_success_response(self)
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
