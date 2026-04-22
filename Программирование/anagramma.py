import random
from tkinter import *

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
    proverit.config(command=check_otvet)

# окно
root = Tk()
root.title("Игра в анаграммы")
root.geometry("200x250")

# элементы
Label(root, text="Анаграмма слова:").pack(padx=1)
anagram_slova = Label(root, font=('Arial', 18), fg='blue')
anagram_slova.pack(pady=10)

Label(root, text="Ваше имя:").pack()
name_igrok= Entry(root, width=20)
name_igrok.pack(pady=5)

Label(root, text="Ваш ответ:").pack()
otvet_igrok = Entry(root, width=20)
otvet_igrok.pack(pady=5)

proverit = Button(root, text="Проверить")
proverit.pack(pady=10)

result_label = Label(root, font=('Arial', 14))
result_label.pack(pady=10)

# играем первый раз
igra()

# запускаем прогу
root.mainloop()

# таблицу рекордов
print("Таблица рекордов:")
for name, score in scores_dict.items():
    print(name, "-", score, "очков")

# находим игрока с наибольшим количеством очков
winner = max(scores_dict, key=scores_dict.get)
print("Победитель:", winner, "со счетом", scores_dict[winner], "очков.")