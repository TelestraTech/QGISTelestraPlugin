"""One-time local download server. Serves only the plugin ZIP, never job files."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import socket
ARCHIVE=Path(__file__).with_name('equipment-library-v0.1.0.zip')
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?',1)[0] != '/equipment-library-v0.1.0.zip':
            self.send_error(404);return
        content=ARCHIVE.read_bytes()
        self.send_response(200);self.send_header('Content-Type','application/zip');self.send_header('Content-Length',str(len(content)));self.end_headers();self.wfile.write(content)
    def log_message(self,fmt,*args):print(fmt%args)
def addresses():
    result=set()
    for item in socket.getaddrinfo(socket.gethostname(),None,socket.AF_INET):
        ip=item[4][0]
        if not ip.startswith(('127.','169.254.')):result.add(ip)
    return sorted(result)
if __name__=='__main__':
    if not ARCHIVE.is_file():raise SystemExit('Keep the plugin ZIP beside this installer script.')
    server=ThreadingHTTPServer(('0.0.0.0',8766),Handler)
    print('\nONE-TIME QFIELD PLUGIN INSTALLATION\nKeep iPhone and this computer on the same Wi-Fi.\n')
    for ip in addresses():print('Install URL: http://'+ip+':8766/equipment-library-v0.1.0.zip')
    print('\nOn iPhone: QField > Settings > Plugins > Install plugin from URL.\nEnter the appropriate Install URL above. Then enable Equipment Library (Pilot).\nIf Windows asks, allow this helper on your private Wi-Fi network.\nClose this window when installation finishes. It is not needed for new jobs.\n')
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
