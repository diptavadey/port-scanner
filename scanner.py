import socket
from datetime import datetime

def scan_ports(target_ip, port_range_start, port_range_end):
    open_ports = []
    
    # Common port labels for better UI reporting
    common_ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 443: "HTTPS", 3306: "MySQL",
        3389: "RDP", 8080: "HTTP-Proxy"
    }

    try:
        for port in range(port_range_start, port_range_end + 1):
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set a timeout so we don't wait forever on closed ports
            s.settimeout(0.5) 
            
            # Returns 0 if the connection is successful
            result = s.connect_ex((target_ip, port))
            if result == 0:
                service = common_ports.get(port, "Unknown Service")
                open_ports.append({"port": port, "service": service})
            s.close()
            
    except Exception as e:
        return {"error": str(e)}

    return open_ports