import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Crear una clase para el servidor web
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, world! This is your web server.')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

# Crear un servidor web en el puerto 8081 (cambiado desde 8080)
def run_web_server(port=8082):  # Modificado para aceptar un argumento de puerto
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f'Web server is running on port {port}...')  # Mostrar el puerto utilizado
    httpd.serve_forever()

# Ejecutar el servidor web en un hilo separado
web_server_thread = threading.Thread(target=run_web_server)
web_server_thread.start()
