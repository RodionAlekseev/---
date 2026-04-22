from tkinter import *
import random

# список слов
slova = ['парадокс', 'парад', 'груша', 'вода', 'макет', 'таро']

# словарь анаграмм
help = {'парадокс': 'ксадорпа', 'парад': 'прада', 'груша': 'шугар', 'вода': 'вдоа', 'макет': 'ткаем', 'таро': 'арот'}

# словарь рекордов
scores_dict = {}

# функция для перемешивания букв в слове
def peremshlova(word):
    letters = list(word)
    random.shuffle(letters)
    return ''.join(letters)

# функция для игры
def igra():

    # случайное слово
    word = random.choice(slova)

    # выводим анаграмму
    anagram_slova.config(text=peremshlova(word))

    # функция для проверки ответа
    def check_otvet():
        otvet = otvet_igrok.get().lower()
        if otvet == word:
            result_label.config(text="Вы угадали!")

            # добавляем очки игроку
            name = name_igrok.get().strip()
            if name:
                if name not in scores_dict:
                    scores_dict[name] = 0
                scores_dict[name] += 10
        else:
            result_label.config(text="Вы не угадали.")

        # очищаем поля для ввода
        name_igrok.delete(0, END)
        otvet_igrok.delete(0, END)

        # играем еще раз
        igra()
        
    # обновляем функцию для кнопки проверки ответа
    prov.config(command=check_otvet)

        
def okno_table():
    novoe_okno = Toplevel(root)
    novoe_okno.geometry('200x100')
    label = Label(novoe_okno)
    label.pack()
    

# окно
root = Tk()
root.title("Game")
root.geometry('200x250')
root.resizable(False, False)



lab1 = Label(root, text = "Анаграмма слова")
lab1.pack()

anagram_slova = Label(root, font=('Arial', 18), fg='orange')
anagram_slova.pack()

lab2 = Label(root, text = 'Ваше имя')
lab2.pack()

name_igrok= Entry(root, width=20, show="")
name_igrok.pack()


lab3 = Label(root, text = 'Ваше слово')
lab3.pack()

otvet_igrok = Entry(root, width=20)
otvet_igrok.pack()

prov = Button(root, text = 'Проверить')
prov.pack()

result_label = Label(root, font=('Arial', 14))
result_label.pack()

okno_people = Button(root, text = 'Таблица лидеров', command= okno_table)
okno_people.pack()

# играем первый раз
igra()

root.mainloop()

# таблицу рекордов
print("Таблица рекордов:")
for name, score in scores_dict.items():
    print(name, "-", score, "очков")

# находим игрока с наибольшим количеством очков
winner = max(scores_dict, key=scores_dict.get)
print("Победитель:", winner, "со счетом", scores_dict[winner], "очков.")