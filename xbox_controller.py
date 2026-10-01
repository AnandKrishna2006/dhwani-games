import socket
import vgamepad as vg
import time

# --- CONFIGURATION ---
UDP_IP = "0.0.0.0"
UDP_PORT = 8080
DEADZONE = 4000  

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Spin up the Virtual Xbox 360 Controller
print("Plugging in Virtual Xbox Controller...")
gamepad = vg.VX360Gamepad()
time.sleep(2)  # Give Windows 2 seconds to recognize the new "USB" device
print("Controller active. Bypassing Chrome sandbox...")

while True:
    try:
        data, _ = sock.recvfrom(1024)
        message = data.decode('utf-8').strip()
        
        if message.startswith("Tilt X:"):
            parts = message.replace("Tilt X:", "").replace("Tilt Y:", "").split("|")
            x_tilt = int(parts[0].strip())
            
            # We trigger BOTH the D-Pad and the Left Joystick to guarantee 
            # maximum compatibility with any web game you choose.
            
            if x_tilt < -DEADZONE:
                # Steer Left
                gamepad.directional_pad(direction=vg.VG_DPAD_LEFT)
                gamepad.left_joystick_float(x_value_float=-1.0, y_value_float=0.0)
                print("<--- LEFT")
                
            elif x_tilt > DEADZONE:
                # Steer Right
                gamepad.directional_pad(direction=vg.VG_DPAD_RIGHT)
                gamepad.left_joystick_float(x_value_float=1.0, y_value_float=0.0)
                print("RIGHT --->")
                
            else:
                # Neutral Deadzone
                gamepad.directional_pad(direction=vg.VG_DPAD_NONE)
                gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
            
            # Send the physical state to Windows
            gamepad.update()
            
    except KeyboardInterrupt:
        print("\nUnplugging Virtual Controller...")
        break
    except Exception:
        pass