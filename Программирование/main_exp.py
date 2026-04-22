import tkinter as tk
import random
from tkinter import messagebox as mb
import csv

score = 0
def Help():
    mb.showinfo('Помощь','''Игра-тренажер "Репетитор по английскому"\nПереводите слова и получайте баллы\nКнопка "Помощь" - первая буква слова\n
Кнопка "Переключить" - меняет направление перевода\nКнопка "Таймер" - запускает игру на время''')

def About():
    mb.showinfo('О программе','Демо-игра для ПИб21')
def Start ():
    global word
    word = random.choice(list(s.keys()))
    ent.delete(0,'end')
    lbl.configure(text = "Переведите слово \"{}\" на английский".format(word))    
def inLabel(event):
    global score,word
    answer = ent.get().lower()
    if answer == s[word].lower():
        score += 1
        lb2.configure(text = 'Бинго! Ваши баллы {}'.format(score))
    else:
        lb2.configure(text = 'Увы. Верный ответ - {}. Ваши баллы {}'.format(s[word],score))
    Start()
    
root = tk.Tk()
root.title('Репетитор по английскому')
root.geometry("430x500+520+100")
root.resizable(False, False)
mainmenu = tk.Menu(root)
root.config(menu=mainmenu) 

filename = tk.PhotoImage(file = "bg.png")
background_label = tk.Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1) 
 
helpmenu = tk.Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь", command = Help)
helpmenu.add_command(label="О программе", command = About)
helpmenu.add_command(label="Рекорды", command = Help) #заглушка
 
mainmenu.add_cascade(label="Справка", menu=helpmenu)
 
ent = tk.Entry(width=38, font="Verdana 12", justify="center")
ent.focus_set() #устанавливаем курсор в поле
ent.place(x=25, y = 200)
s = {}
with open("base_it.csv",  encoding="utf-8") as File:
    reader = csv.reader(File, delimiter=';', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        s[row[0]] = row[1]
        

lbl = tk.Label(height=2,  font="Verdana 10", bg='black', fg="white", justify="center")
lbl.place(x=30, y=110)
Start()
lb2 = tk.Label(height=2, font="Verdana 10", bg='white')
lb2.place(x=30, y=35)
ent.bind('<Return>',inLabel)
root.mainloop()
