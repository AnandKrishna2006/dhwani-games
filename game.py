import pygame
import socket
import sys

# --- UDP NETWORK SETUP ---
UDP_IP = "0.0.0.0"
UDP_PORT = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)  # Prevents the network from freezing the game graphics

# --- PYGAME SETUP ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RISE CET: Direct UDP Telemetry")
clock = pygame.time.Clock()

# Game variables
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_radius = 25
DEADZONE = 4000
SPEED = 10  # How fast the ball moves side to side

print("Local Game Engine Running. Awaiting Wi-Fi Telemetry...")

running = True
while running:
    # 1. Handle closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Read direct Wi-Fi telemetry (No keyboard emulation needed!)
    try:
        data, _ = sock.recvfrom(1024)
        message = data.decode('utf-8').strip()
        
        if message.startswith("Tilt X:"):
            parts = message.replace("Tilt X:", "").replace("Tilt Y:", "").split("|")
            x_tilt = int(parts[0].strip())
            
            # Move the ball directly based on raw data
            if x_tilt < -DEADZONE:
                player_x -= SPEED
            elif x_tilt > DEADZONE:
                player_x += SPEED
                
    except BlockingIOError:
        pass  # No new packet this frame, just keep drawing
    except Exception:
        pass

    # Keep player on screen
    if player_x < player_radius: player_x = player_radius
    if player_x > WIDTH - player_radius: player_x = WIDTH - player_radius

    # 3. Draw the Graphics
    screen.fill((20, 20, 30))  # Dark background
    
    # Draw the ball (Cyan)
    pygame.draw.circle(screen, (0, 255, 255), (player_x, player_y), player_radius)
    
    # Draw a "Target" zone for aesthetics
    pygame.draw.rect(screen, (100, 100, 100), (0, HEIGHT - 50, WIDTH, 50))

    pygame.display.flip()
    clock.tick(60) # Run at 60 FPS

pygame.quit()
sys.exit()