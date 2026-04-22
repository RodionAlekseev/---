
from tkinter import *
import random

# список слов для игры
slova = ['молоко', 'город', 'река', 'лес', 'деньги', 'кот', 'ковер', 'парта', 'птица', 'картошка']

# словарь с рекордами
records = {}

# главное окно
root = Tk()
root.title('Игра "Анаграмма"')

# функция для перемешивания букв в слове
def shuffle_word(word):
    word = list(word)
    random.shuffle(word)
    return ''.join(word)

# функция для проверки ответа
def check_answer():
    user_answer = answer_entry.get().strip().lower()
    if user_answer == word:
        status_label.config(text='Ответ правильный!', fg='green')
        add_score()
        new_word()
    else:
        status_label.config(text='Ответ неправильный!', fg='red')

# функция для добавления очков
def add_score():
    global score
    score += 1
    score_label.config(text=f'Очки: {score}')

# функция для сохранения рекорда
def save_record():
    global score
    name = name_entry.get().strip()
    if name:
        records[name] = score
        with open('records.txt', 'w', encoding='utf-8') as f:
            for name, score in records.items():
                f.write(f'{name}: {score}\n')
        message_label.config(text='Рекорд сохранен!', fg='green')
    else:
        message_label.config(text='Введите имя!', fg='red')

# функция для вывода таблицы лидеров
def show_records():
    with open('records.txt', 'r', encoding='utf-8') as f:
        records_text = f.read()
        records_window = Toplevel(root)
        records_window.title('Таблица лидеров')
        records_label = Label(records_window, text=records_text, font=('Arial', 12))
        records_label.pack()

# функция для выбора нового слова и отображения его на экране
def new_word():
    global word
    word = random.choice(slova)
    while len(set(word)) == 1: # проверка на повторяющиеся буквы в слове
        word = random.choice(slova)
    shuffled_word = shuffle_word(word)
    word_label.config(text=shuffled_word)
    answer_entry.delete(0, END)
    status_label.config(text='')

# окно ввода имени для сохранения рекорда
name_window = Toplevel(root)
name_window.title('Введите имя')

name_label = Label(name_window, text='Введите имя:', font=('Arial', 12))
name_label.pack(side=LEFT)

name_entry = Entry(name_window, font=('Arial', 12))
name_entry.pack(side=LEFT)
name_entry.focus()

name_button = Button(name_window, text='Сохранить', font=('Arial', 12), command=save_record)
name_button.pack(side=LEFT)

# главное окно
word_frame = Frame(root)
word_frame.pack(pady=10)

word_label = Label(word_frame, text='', font=('Arial', 24), bg='white', width=15, height=2, bd=10, relief='groove')
word_label.pack(side=LEFT)

answer_entry = Entry(word_frame, font=('Arial', 24), width=15, bd=5)
answer_entry.pack(side=LEFT)

check_button = Button(root, text='Проверить', font=('Arial', 16), command=check_answer)
check_button.pack(pady=10)

status_label = Label(root, text='', font=('Arial', 16))
status_label.pack()

score = 0
score_label = Label(root, text=f'Очки: {score}', font=('Arial', 16))
score_label.pack()

message_label = Label(root, text='', font=('Arial', 16))
message_label.pack()

records_button = Button(root, text='Таблица лидеров', font=('Arial', 16), command=show_records)
records_button.pack(pady=10)

# запуск игры
new_word()
root.mainloop()