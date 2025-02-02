# import os
# import time
# import threading
# import customtkinter as ctk
# from PIL import ImageGrab

# # Create the main application window
# app = ctk.CTk()
# app.title("Screen Capture Tool")

# # Get screen width and height
# screen_width = app.winfo_screenwidth()
# screen_height = app.winfo_screenheight()

# # Set window size
# window_width = 600
# window_height = 400

# # Calculate position to center the window
# position_x = (screen_width - window_width) // 2
# position_y = (screen_height - window_height) // 2

# app.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

# folder_name = "cap_img"
# os.makedirs(folder_name, exist_ok=True)

# capture_interval = 5  # Default interval in seconds
# capturing = False  # Flag to control capturing

# def capture_full_screen():
#     global capturing
#     while capturing:
#         screenshot = ImageGrab.grab()
#         timestamp = time.strftime("%Y%m%d_%H%M%S")
#         file_name = os.path.join(folder_name, f"1-{timestamp}.png")
#         screenshot.save(file_name)
#         print(f"Captured: {file_name}")
#         time.sleep(capture_interval)

# def start_capture():
#     global capturing
#     if not capturing:
#         capturing = True
#         threading.Thread(target=capture_full_screen, daemon=True).start()

# def stop_capture():
#     global capturing
#     capturing = False

# def increase_time():
#     global capture_interval
#     capture_interval += 5
#     time_label.configure(text=f"Interval: {capture_interval} sec")

# def decrease_time():
#     global capture_interval
#     if capture_interval > 5:
#         capture_interval -= 5
#         time_label.configure(text=f"Interval: {capture_interval} sec")


# time_label = ctk.CTkLabel(app, text=f"Interval: {capture_interval} sec", font=("Arial", 16,"bold"), text_color="#58a6ff")
# time_label.pack(pady=40)

# # Directly adding buttons without a frame
# start_button = ctk.CTkButton(app, text="Start Capture", command=start_capture, font=("Arial", 14, "bold"), 
#                               fg_color="#238636", text_color="white", hover_color="#2a9d60",width=250, height=35)
# start_button.pack(pady=13)

# stop_button = ctk.CTkButton(app, text="Stop Capture", command=stop_capture, font=("Arial", 14, "bold"), 
#                              fg_color="#da3633", text_color="white", hover_color="#e84a47" , width=250, height=35)
# stop_button.pack(pady=13)

# increase_button = ctk.CTkButton(app, text="Increase Interval", command=increase_time, font=("Arial", 14, "bold"), 
#                                 fg_color="#8957e5", text_color="white", hover_color="#9b6bf5" , width=250, height=35)
# increase_button.pack(pady=13)

# decrease_button = ctk.CTkButton(app, text="Decrease Interval", command=decrease_time, font=("Arial", 14, "bold"), 
#                                 fg_color="#d29922", text_color="white", hover_color="#f7b34c" , width=250, height=35)
# decrease_button.pack(pady=13)

# app.mainloop()

import os
import time
import threading
import customtkinter as ctk
from PIL import ImageGrab

# Create the main application window
app = ctk.CTk()
app.title("Screen Capture Tool")

# Get screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Set window size
window_width = 600
window_height = 400

# Calculate position to center the window
position_x = (screen_width - window_width) // 2
position_y = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

folder_name = "cap_img"
os.makedirs(folder_name, exist_ok=True)

capture_interval = 5  # Default interval in seconds
capturing = False  # Flag to control capturing

def capture_full_screen():
    global capturing
    while capturing:
        screenshot = ImageGrab.grab()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = os.path.join(folder_name, f"1-{timestamp}.png")
        screenshot.save(file_name)
        print(f"Captured: {file_name}")
        time.sleep(capture_interval)

def start_capture():
    global capturing
    if not capturing:
        capturing = True
        threading.Thread(target=capture_full_screen, daemon=True).start()
        app.iconify()  # Minimize the window when capture starts

def stop_capture():
    global capturing
    capturing = False

def increase_time():
    global capture_interval
    capture_interval += 5
    time_label.configure(text=f"Interval: {capture_interval} sec")

def decrease_time():
    global capture_interval
    if capture_interval > 5:
        capture_interval -= 5
        time_label.configure(text=f"Interval: {capture_interval} sec")


time_label = ctk.CTkLabel(app, text=f"Interval: {capture_interval} sec", font=("Arial", 16, "bold"), text_color="#58a6ff")
time_label.pack(pady=40)

# Directly adding buttons without a frame
start_button = ctk.CTkButton(app, text="Start Capture", command=start_capture, font=("Arial", 14, "bold"), 
                              fg_color="#238636", text_color="white", hover_color="#2a9d60", width=250, height=35)
start_button.pack(pady=13)

stop_button = ctk.CTkButton(app, text="Stop Capture", command=stop_capture, font=("Arial", 14, "bold"), 
                             fg_color="#da3633", text_color="white", hover_color="#e84a47", width=250, height=35)
stop_button.pack(pady=13)

increase_button = ctk.CTkButton(app, text="Increase Interval", command=increase_time, font=("Arial", 14, "bold"), 
                                fg_color="#8957e5", text_color="white", hover_color="#9b6bf5", width=250, height=35)
increase_button.pack(pady=13)

decrease_button = ctk.CTkButton(app, text="Decrease Interval", command=decrease_time, font=("Arial", 14, "bold"), 
                                fg_color="#d29922", text_color="white", hover_color="#f7b34c", width=250, height=35)
decrease_button.pack(pady=13)

app.mainloop()
