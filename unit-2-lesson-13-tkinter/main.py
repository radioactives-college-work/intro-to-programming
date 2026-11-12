import tkinter as tk
from tkinter import messagebox

def convert(event=None):
    try:
        celsius = float(temp_entry.get())
        fahrenheit = celsius * 1.8 + 32
        result_label.config(text=str(fahrenheit))
    except ValueError:
        messagebox.showerror(message="Please enter only\nnumerical values.")
def clear():
    temp_entry.delete(0, tk.END)


window = tk.Tk()
window.title("Temperature Converter")
window.geometry("450x350")

tk.Label(window, text="Celsius").grid(row=0, column=0, padx=10, pady=10)
temp_entry = tk.Entry(window)
temp_entry.grid(row=0, column=1, pady=10, padx=10)

convert_button = tk.Button(window, text="Convert", command=convert)
convert_button.grid(row=1, column=0, padx=10, pady=10)

clear_button = tk.Button(window, text="Clear", command=clear)
clear_button.grid(row=1, column=1, padx=10, pady=10)
result_label = tk.Label(window)
result_label.grid(row=2, column=0, padx=10, pady=10)

window.bind("<Return>", convert)

window.mainloop()