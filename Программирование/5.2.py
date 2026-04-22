from tkinter import *

# увеличения размера поля
def bolshe(event):
    current_width = pole.config()['width'][-1]
    pole.config(width=current_width + 2)

# уменьшения размера поля
def menshe(event):
    current_width = pole.config()['width'][-1]
    pole.config(width=max(2, current_width - 2))

# возвращает к исходному размеру поля
def vernyt(event):
    pole.config(width=20)

root = Tk()

pole= Entry(root, width=20)
pole.pack()


pole.bind("<Button-1>", menshe)
pole.bind("<Button-2>", vernyt)
pole.bind("<Button-3>", bolshe)

root.mainloop()