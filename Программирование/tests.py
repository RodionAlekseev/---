from tkinter import *
from tkinter import ttk
 
def show_message():
    label["text"] = entry.get()     # получаем введенный текст
 
root = Tk()
root.title("METANIT.COM")
root.geometry("250x200") 
 
entry = ttk.Entry()
entry.pack(anchor=NW, padx=6, pady=6)
  
btn = ttk.Button(text="Click", command=show_message)
btn.pack(anchor=NW, padx=6, pady=6)
 
label = ttk.Label()
label.pack(anchor=NW, padx=6, pady=6)
  
root.mainloop()