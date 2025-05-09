from http.server import BaseHTTPRequestHandler
from app import app
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Import Flask app
        with app.test_client() as client:
            response = client.get(self.path)
            self.wfile.write(response.data)
            return
            
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Import Flask app
        with app.test_client() as client:
            response = client.post(
                self.path, 
                data=post_data, 
                content_type='application/x-www-form-urlencoded'
            )
            self.wfile.write(response.data)
            return