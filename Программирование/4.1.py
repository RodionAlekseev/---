from tkinter import *

t = 0

def printer(event):
    global t
    t +=1
    print("Вы нажали на кнопку {} раз".format(t))

root = Tk()
but = Button(root, text = "Нажми меня, мне это нравится!".format(t))
but.bind("<Button-1> ", printer)
but.pack()

root.mainloop()
