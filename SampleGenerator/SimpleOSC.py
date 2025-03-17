from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client
from pythonosc import osc_server
import threading

# install the python-osc library first with: pip install python-osc

class SimpleOSC:
    def __init__(self, send_ip="127.0.0.1", send_port=9000, receive_port=8000):
        self.client = udp_client.SimpleUDPClient(send_ip, send_port)
        self.dispatcher = Dispatcher()
        self.server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", receive_port), self.dispatcher)
        self.server_thread = None

    def on(self, address, handler):
        """Bind a handler function to an OSC address."""
        self.dispatcher.map(address, handler)

    def start(self):
        """Start the OSC server in a separate thread."""
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def send(self, address, *args):
        """Send an OSC message."""
        self.client.send_message(address, args)

    def stop(self):
        """Stop the OSC server."""
        if self.server_thread:
            self.server.shutdown()
            self.server_thread.join()

# Example usage
if __name__ == "__main__":
    def handle_osc(address, *args):
        print(f"Received: {address}, {args}")

    osc = SimpleOSC()

    # Add a handler for incoming messages
    osc.on("/test", handle_osc)

    # Start the server
    osc.start()

    # Send a test message
    osc.send("/test", "hello", 42)

    try:
        input("Press Enter to exit...\n")
    finally:
        osc.stop()
