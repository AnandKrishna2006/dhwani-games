import socket
import pyautogui

# --- CONFIGURATION ---
UDP_IP = "0.0.0.0"
UDP_PORT = 8080
GYRO_DEADZONE = 400   # Ignores natural hand shaking. Increase if the cursor drifts when still.
SENSITIVITY = 100.0   # Lower number = faster aiming. Higher number = slower, precise aiming.

# --- SCREEN SETUP ---
pyautogui.FAILSAFE = False
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
FIXED_Y = SCREEN_HEIGHT // 2  # Locks the crosshair to the middle horizontal line

# Start the cursor in the center of the screen
cursor_x = SCREEN_WIDTH // 2  

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Air-Gun Backend Running on a {SCREEN_WIDTH}x{SCREEN_HEIGHT} display.")
print("Waiting for ESP32 telemetry...")

is_trigger_pulled = False

while True:
    try:
        data, _ = sock.recvfrom(1024)
        message = data.decode('utf-8').strip()
        
        if message.startswith("GyZ:"):
            parts = message.split("|")
            
            gyz = int(parts[0].replace("GyZ:", "").strip())
            trigger = int(parts[1].replace("Trigger:", "").strip())
            
            # --- 1. HORIZONTAL PANNING ---
            if abs(gyz) > GYRO_DEADZONE:
                # We add the gyro velocity to the current cursor position.
                # NOTE: If aiming left makes the cursor go right, change this `-=` to `+=`
                cursor_x -= (gyz / SENSITIVITY)
            
            # Clamp the math so the cursor doesn't get stuck off-screen
            cursor_x = max(0, min(SCREEN_WIDTH, cursor_x))
            
            # Enforce the Y-axis lock and move the mouse
            pyautogui.moveTo(int(cursor_x), FIXED_Y, _pause=False)
            
            # --- 2. FIRING MECHANISM ---
            # Trigger is 0 when pressed (INPUT_PULLUP)
            if trigger == 0 and not is_trigger_pulled:
                pyautogui.click()
                is_trigger_pulled = True
                print(f"BANG! (Fired at X: {int(cursor_x)})")
                
            elif trigger == 1 and is_trigger_pulled:
                is_trigger_pulled = False # Reset the trigger logic for the next shot
                
    except KeyboardInterrupt:
        print("\nBackend stopped.")
        break
    except Exception:
        pass # Ignore garbled Wi-Fi packets