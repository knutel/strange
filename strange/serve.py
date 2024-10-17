import http.server
import socketserver
import threading
from watchfiles import watch


class Server:
    def __init__(self, folder, port):
        self.folder = folder
        self.port = port

    def start(self):
        self.thread = threading.Thread(target=self.run_server)
        self.thread.start()

    def run_server(self):
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(innerself, *args, **kwargs):
                super().__init__(*args, directory=self.folder, **kwargs)

        with socketserver.TCPServer(("", self.port), Handler) as httpd:
            self.server = httpd
            print("serving at port", self.port)
            httpd.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.thread.join()

def watch_and_serve(process, folder, port):
    server = Server(folder, port)
    server.start()

    while True:
        process(folder)
        try:
            for changes in watch("content"):
                print(changes)
                break
        except KeyboardInterrupt:
            break
