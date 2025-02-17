import os
import time
import threading
import cv2
import numpy as np
import pyautogui
import pyaudio
import customtkinter as ctk
from PIL import ImageGrab

# Initialize main application window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Screen Capture & Recorder")
#window resizable
app.resizable(False,False)

# Window dimensions
window_width, window_height = 600, 550
screen_width, screen_height = app.winfo_screenwidth(), app.winfo_screenheight()
position_x, position_y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
app.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

# Create necessary folders
screenshot_folder, video_folder = "cap_img", "Screen-Video"
os.makedirs(screenshot_folder, exist_ok=True)
os.makedirs(video_folder, exist_ok=True)

capture_interval, capturing, recording = 5, False, False

def capture_full_screen():
    global capturing
    while capturing:
        screenshot = ImageGrab.grab()
        file_name = os.path.join(screenshot_folder, f"1-{time.strftime('%Y%m%d_%H%M%S')}.png")
        screenshot.save(file_name)
        time.sleep(capture_interval)

def toggle_capture():
    global capturing
    capturing = not capturing
    if capturing:
        threading.Thread(target=capture_full_screen, daemon=True).start()
        app.iconify()

def stop_capture():
    global capturing
    capturing = False

def change_interval(delta):
    global capture_interval
    capture_interval = max(5, capture_interval + delta)
    time_label.configure(text=f"Interval: {capture_interval} sec")

def toggle_recording():
    global recording
    recording = not recording
    if recording:
        threading.Thread(target=record_video_audio, daemon=True).start()
        app.iconify()

def stop_recording():
    global recording
    recording = False

def record_video_audio():
    global recording
    video_filename = os.path.join(video_folder, f"record-{time.strftime('%Y%m%d_%H%M%S')}.mp4")
    out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*"mp4v"), 20.0, (screen_width, screen_height))
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    
    while recording:
        frame = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
        out.write(frame)
        stream.read(1024)
    
    out.release()
    stream.stop_stream()
    stream.close()
    audio.terminate()

# UI Layout
ctk.CTkLabel(app, text="Screen Capture & Recorder", font=("Arial", 20, "bold"), text_color="#58a6ff").pack(pady=15)

time_label = ctk.CTkLabel(app, text=f"Interval: {capture_interval} sec", font=("Arial", 16))
time_label.pack(pady=5)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20, padx=20, fill="both", expand=True)

buttons = [
    ("Start Capture", lambda: toggle_capture(), "#238636"),
    ("Stop Capture", lambda: stop_capture(), "#da3633"),
    ("Increase Interval", lambda: change_interval(5), "#8957e5"),
    ("Decrease Interval", lambda: change_interval(-5), "#d29922"),
    ("Start Recording", lambda: toggle_recording(), "#0078D7"),
    ("Stop Recording", lambda: stop_recording(), "#FF5733"),
]

for i in range(0, len(buttons), 2):
    row_frame = ctk.CTkFrame(button_frame)
    row_frame.pack(pady=10)
    for text, command, color in buttons[i:i+2]:
        ctk.CTkButton(row_frame, text=text, command=command, fg_color=color, width=250, height=40).pack(side="left", padx=10)

app.mainloop()