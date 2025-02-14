import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2docx import Converter
import os

def select_pdf():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")],
        title="Select a PDF file"
    )
    if file_path:
        pdf_path.set(file_path)

def convert_pdf_to_word():
    pdf_file = pdf_path.get()
    if not pdf_file:
        messagebox.showwarning("No File Selected", "Please select a PDF file first.")
        return

    # Setting default output filename
    word_file = os.path.splitext(pdf_file)[0] + '.docx'

    try:
        cv = Converter(pdf_file)
        cv.convert(word_file, start=0, end=None)
        cv.close()
        messagebox.showinfo("Success", f"PDF converted successfully!\nSaved as: {word_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

# Create the main window
root = tk.Tk()
root.title("PDF to Word Converter")
root.geometry("400x200")
root.resizable(False, False)

# Variables
pdf_path = tk.StringVar()

# UI Components
tk.Label(root, text="PDF to Word Converter", font=("Arial", 16, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Entry(frame, textvariable=pdf_path, width=40, state='readonly').grid(row=0, column=0, padx=5)
tk.Button(frame, text="Browse", command=select_pdf).grid(row=0, column=1, padx=5)

tk.Button(root, text="Convert to Word", command=convert_pdf_to_word, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=20)

# Run the application
root.mainloop()
