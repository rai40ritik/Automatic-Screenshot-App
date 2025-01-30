import time
import os
from PIL import ImageGrab

def capture_full_screen():
    # Create a folder named 'cap_img' if it doesn't exist
    folder_name = "cap_img"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    while True:
        # Capture the entire screen
        screenshot = ImageGrab.grab()

        # Save the screenshot with a timestamp in the 'cap_img' folder
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = os.path.join(folder_name, f"full_screen_img_{timestamp}.png")
        screenshot.save(file_name)

        print(f"Captured: {file_name}")

        # Wait for 15 seconds before capturing again
        time.sleep(15)

if __name__ == "__main__":
    print("Starting full screen capture every 15 seconds. Press Ctrl+C to stop.")
    try:
        capture_full_screen()
    except KeyboardInterrupt:
        print("Stopped full screen capture.")
