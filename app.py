from flask import Flask, render_template, request
import socket

app = Flask(__name__)

def perform_scan(target, start_port, end_port):
    open_ports = []
    # Common port mapping
    services = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 443: "HTTPS", 3306: "MySQL"}
    
    for port in range(start_port, end_port + 1):
        try:
            # Create a socket to test the connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3) # Fast scan
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append({
                    "port": port,
                    "service": services.get(port, "Unknown")
                })
            sock.close()
        except:
            continue
    return open_ports

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    target_ip = ""
    if request.method == 'POST':
        target_ip = request.form.get('target')
        # Scanning ports 1 through 500 for speed
        results = perform_scan(target_ip, 1, 500)
        
    return render_template('scanner.html', results=results, target=target_ip)

if __name__ == '__main__':
    app.run(debug=True)