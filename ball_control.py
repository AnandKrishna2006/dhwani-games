import socket
import keyboard
import time  # <-- 1. Added the time library

# --- CONFIGURATION ---
UDP_IP = "0.0.0.0"
UDP_PORT = 8080
DEADZONE = 4000  

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Hardware Keyboard Driver Running (Analog Tap Mode).")
print("Stand on the board and keep it flat...")

while True:
    try:
        data, _ = sock.recvfrom(1024)
        message = data.decode('utf-8').strip()
        
        if message.startswith("Tilt X:"):
            parts = message.replace("Tilt X:", "").replace("Tilt Y:", "").split("|")
            x_tilt = int(parts[0].strip())
            
            # --- ANALOG TAP LOGIC ---
            
            if x_tilt < -DEADZONE:
                keyboard.press('left')
                time.sleep(0.03)          # Hold for 30 milliseconds
                keyboard.release('left')  # Instantly release
                print("<--- TAP LEFT")
                    
            elif x_tilt > DEADZONE:
                keyboard.press('right')
                time.sleep(0.03)          # Hold for 30 milliseconds
                keyboard.release('right') # Instantly release
                print("TAP RIGHT --->")
                    
            else:
                # Neutral Deadzone
                # We don't need release commands here anymore because 
                # the keys automatically release themselves after 30ms!
                pass
                
    except KeyboardInterrupt:
        # Safety cleanup
        keyboard.release('left')
        keyboard.release('right')
        print("\nEmulator stopped.")
        break
    except Exception:
        pass