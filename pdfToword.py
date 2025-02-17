import customtkinter as ctk
from tkinter import filedialog, messagebox
from pdf2docx import Converter
from docx2pdf import convert
import os
import threading

def select_pdf():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")],
        title="Select a PDF file"
    )
    if file_path:
        pdf_path.set(file_path)

def select_word():
    file_path = filedialog.askopenfilename(
        filetypes=[("Word Files", "*.docx")],
        title="Select a Word file"
    )
    if file_path:
        word_path.set(file_path)

def convert_pdf_to_word():
    pdf_file = pdf_path.get()
    if not pdf_file:
        messagebox.showwarning("No File Selected", "Please select a PDF file first.")
        return
    
    word_file = os.path.splitext(pdf_file)[0] + '.docx'
    
    def convert():
        convert_button.configure(state="disabled", text="Converting...")
        try:
            cv = Converter(pdf_file)
            cv.convert(word_file, start=0, end=None)
            cv.close()
            messagebox.showinfo("Process Completed", "PDF converted successfully!\nSaved as: {}".format(word_file))
        except Exception as e:
            messagebox.showerror("Error", "An error occurred:\n{}".format(str(e)))
        finally:
            convert_button.configure(state="normal", text="Convert to Word")
    
    threading.Thread(target=convert, daemon=True).start()

def convert_word_to_pdf():
    word_file = word_path.get()
    if not word_file:
        messagebox.showwarning("No File Selected", "Please select a Word file first.")
        return
    
    pdf_file = os.path.splitext(word_file)[0] + '.pdf'
    
    def convert():
        word_to_pdf_button.configure(state="disabled", text="Converting...")
        try:
            convert(word_file, pdf_file)
            messagebox.showinfo("Process Completed", "Word converted successfully!\nSaved as: {}".format(pdf_file))
        except Exception as e:
            messagebox.showerror("Error", "An error occurred:\n{}".format(str(e)))
        finally:
            word_to_pdf_button.configure(state="normal", text="Convert to PDF")
    
    threading.Thread(target=convert, daemon=True).start()

# Create the main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("PDF & Word Converter")
root.state("zoomed")  # Open in full-screen mode
root.resizable(True, True)

# Variables
pdf_path = ctk.StringVar()
word_path = ctk.StringVar()

# UI Components
title_label = ctk.CTkLabel(root, text="PDF & Word Converter", font=("Arial", 20, "bold"))
title_label.pack(pady=15)

frame = ctk.CTkFrame(root)
frame.pack(pady=10, padx=10)

entry = ctk.CTkEntry(frame, textvariable=pdf_path, width=300, state='readonly')
entry.grid(row=0, column=0, padx=5, pady=5)

browse_button = ctk.CTkButton(frame, text="Browse PDF", command=select_pdf)
browse_button.grid(row=0, column=1, padx=5, pady=5)

convert_button = ctk.CTkButton(root, text="Convert to Word", command=convert_pdf_to_word, fg_color="#4CAF50", text_color="white", font=("Arial", 14))
convert_button.pack(pady=10)

frame2 = ctk.CTkFrame(root)
frame2.pack(pady=10, padx=10)

entry2 = ctk.CTkEntry(frame2, textvariable=word_path, width=300, state='readonly')
entry2.grid(row=0, column=0, padx=5, pady=5)

browse_button2 = ctk.CTkButton(frame2, text="Browse Word", command=select_word)
browse_button2.grid(row=0, column=1, padx=5, pady=5)

word_to_pdf_button = ctk.CTkButton(root, text="Convert to PDF", command=convert_word_to_pdf, fg_color="#FF5733", text_color="white", font=("Arial", 14))
word_to_pdf_button.pack(pady=10)

# Run the application
root.mainloop()