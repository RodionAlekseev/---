from tkinter import *

def change():
    if var.get() == 0:
        b1['bg'] = 'red'
        b2['bg'] = '#f0f0f0'
    elif var.get() == 1:
        b1['bg'] = '#f0f0f0'
        b2['bg'] = 'red'

root = Tk()
 
var = IntVar()
var.set(0)

y = Radiobutton(text="Лево",variable=var, value=0)
y.pack(side='bottom')

x = Radiobutton(text="Право", variable=var, value=1)
x.pack(side='bottom')

b1 = Button(text="Нажми", width=15, height=3, command = change)
b1.pack(side=LEFT)


b2 = Button(text="Сюда тоже можно", width=15, height=3, command = change)
b2.pack(side=RIGHT)

root.mainloop()