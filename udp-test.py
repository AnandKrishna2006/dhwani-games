import socket

# Listen on all available network interfaces on port 8080
UDP_IP = "0.0.0.0" 
UDP_PORT = 8080

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Server started. Listening for ESP32 data on port {UDP_PORT}...")
print("Waiting for first packet...\n")

while True:
    try:
        # Buffer size is 1024 bytes
        data, addr = sock.recvfrom(1024)
        
        # Decode the raw bytes into a string and strip whitespace
        message = data.decode('utf-8').strip()
        
        print(f"Packet from {addr[0]}: {message}")
        
    except KeyboardInterrupt:
        print("\nListener stopped.")
        break