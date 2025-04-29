from cx_Freeze import setup, Executable
import sys

# List of folders and files to include
include_files = [
    ("cap_img", "cap_img"),
    ("Screen-Video", "Screen-Video"),
    ("icon.ico", "icon.ico"),
    (r"C:\Windows\System32\vcruntime140.dll", "vcruntime140.dll"),
    (r"C:\Windows\System32\msvcp140.dll", "msvcp140.dll")
]

build_exe_options = {
    "packages": [
        "os", "time", "threading", "cv2", "numpy", "pyautogui",
        "pyaudio", "customtkinter", "PIL.ImageGrab"
    ],
    "include_files": include_files
}

# Set GUI base
base = "Win32GUI" if sys.platform == "win32" else None

# Define the executable
executables = [
    Executable(
        script="app.py",
        base=base,
        target_name="ScreenCaptureRecorder.exe",
        icon="icon.ico"
    )
]

# Final setup configuration
setup(
    name="ScreenCaptureRecorder",
    version="1.0",
    description="A Python-based Screen Capture & Recorder Tool",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": {
            "upgrade_code": "{12345678-ABCD-1234-ABCD-1234567890AB}",
            "add_to_path": False,
            "initial_target_dir": r"[ProgramFilesFolder]\ScreenCaptureRecorder"
        }
    },
    executables=executables
)
