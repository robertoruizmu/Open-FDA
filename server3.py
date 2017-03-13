
import realweb3
import socketserver

PORT=8008

#Handler = http.server.SimpleHTTPRequestHandler
Handler=realweb3.testHTTPRequestHandler
#Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
