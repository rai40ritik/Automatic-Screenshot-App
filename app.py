import os
import time
import threading
import cv2
import numpy as np
import pyautogui
import pyaudio
import wave
import customtkinter as ctk
from PIL import ImageGrab
import subprocess

# Create the main application window
app = ctk.CTk()
app.title("Screen Capture Tool")

# Get screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Set window size
window_width = 600
window_height = 500

# Calculate position to center the window
position_x = (screen_width - window_width) // 2
position_y = (screen_height - window_height) // 2

app.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

# Folders for screenshots and videos
screenshot_folder = "cap_img"
video_folder = "Screen-Video"
os.makedirs(screenshot_folder, exist_ok=True)
os.makedirs(video_folder, exist_ok=True)

capture_interval = 5  # Default interval in seconds
capturing = False  # Flag to control capturing
recording = False  # Flag to control recording

def capture_full_screen():
    global capturing
    while capturing:
        screenshot = ImageGrab.grab()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = os.path.join(screenshot_folder, f"1-{timestamp}.png")
        screenshot.save(file_name)
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

def record_screen():
    global recording
    if not recording:
        recording = True
        threading.Thread(target=record_video_audio, daemon=True).start()
        app.iconify()  # Minimize the window when recording starts

def stop_recording():
    global recording
    recording = False

def record_video_audio():
    global recording
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    video_filename = os.path.join(video_folder, f"temp_video-{timestamp}.avi")
    audio_filename = os.path.join(video_folder, f"temp_audio-{timestamp}.wav")
    final_output = os.path.join(video_folder, f"record-{timestamp}.mp4")
    
    screen_size = (screen_width, screen_height)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(video_filename, fourcc, 20.0, screen_size)
    
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    
    audio_frames = []

    while recording:
        # Capture video frame
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)

        # Capture audio frame
        audio_data = stream.read(1024)
        audio_frames.append(audio_data)
        time.sleep(0.05)
    
    out.release()
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save audio to WAV file
    wf = wave.open(audio_filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(audio_frames))
    wf.close()

    # Combine video and audio using FFmpeg
    merge_video_audio(video_filename, audio_filename, final_output)

    # Clean up temporary files
    os.remove(video_filename)
    os.remove(audio_filename)

def merge_video_audio(video_file, audio_file, output_file):
    command = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Recording saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error merging video and audio: {e}")

# UI Elements
time_label = ctk.CTkLabel(app, text=f"Interval: {capture_interval} sec", font=("Arial", 16, "bold"), text_color="#58a6ff")
time_label.pack(pady=20)

start_button = ctk.CTkButton(app, text="Start Capture", command=start_capture, font=("Arial", 14, "bold"),
                              fg_color="#238636", text_color="white", hover_color="#2a9d60", width=250, height=35)
start_button.pack(pady=10)

stop_button = ctk.CTkButton(app, text="Stop Capture", command=stop_capture, font=("Arial", 14, "bold"),
                             fg_color="#da3633", text_color="white", hover_color="#e84a47", width=250, height=35)
stop_button.pack(pady=10)

increase_button = ctk.CTkButton(app, text="Increase Interval", command=increase_time, font=("Arial", 14, "bold"),
                                fg_color="#8957e5", text_color="white", hover_color="#9b6bf5", width=250, height=35)
increase_button.pack(pady=10)

decrease_button = ctk.CTkButton(app, text="Decrease Interval", command=decrease_time, font=("Arial", 14, "bold"),
                                fg_color="#d29922", text_color="white", hover_color="#f7b34c", width=250, height=35)
decrease_button.pack(pady=10)

record_button = ctk.CTkButton(app, text="Record Window Screen", command=record_screen, font=("Arial", 14, "bold"),
                              fg_color="#0078D7", text_color="white", hover_color="#3399FF", width=250, height=35)
record_button.pack(pady=10)

stop_record_button = ctk.CTkButton(app, text="Stop Window Screen", command=stop_recording, font=("Arial", 14, "bold"),
                                   fg_color="#FF5733", text_color="white", hover_color="#FF704D", width=250, height=35)
stop_record_button.pack(pady=10)

app.mainloop()
