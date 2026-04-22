import tkinter as tk
import random

# Словарь для перевода
dictionary = {'кот': 'cat',
              'собака': 'dog',
              'машина': 'car',
              'дом': 'house',
              'книга': 'book',
              'стол': 'table',
              'компьютер': 'computer',
              'телефон': 'phone',
              'окно': 'window',
              'дверь': 'door',
              'молоко': 'milk',
              'вода': 'water',
              'сок': 'juice',
              'чай': 'tea',
              'кофе': 'coffee'}

#  функция начала игры
def start_game():
    # в начале игры ставим счетчик очков на 10
    score = 10
    score_label.config(text='Очки: ' + str(score))  # отображаем счетчик очков на экране
    answer_entry.delete(0, 'end')  # очищаем поле ввода ответа

    # если список слов закончился, то выводим количество набранных очков на экран и завершаем игру
    if not words_list:
        result_label.config(text='Ваш результат: ' + str(score))
        check_button.config(state='disabled')
        return

    # выбираем случайное слово из списка и показываем его перевод на экране
    word = random.choice(words_list)
    words_list.remove(word)
    word_label.config(text=word)

    # выбираем уровень сложности
    level = difficulty.get()

    # если уровень сложности 'Легко'
    if level == 'Легко':
        # выбираем случайный порядок букв в переводе и показываем его на экране
        translation = dictionary[word]
        shuffled_translation = ''.join(random.sample(translation, len(translation)))
        translation_label.config(text=shuffled_translation)
    # если уровень сложности 'Сложно'
    elif level == 'Сложно':
        # не показываем перевод, а только просим ввести его вручную
        translation_label.config(text='Введите перевод')

    # задаем фокус на поле ввода ответа
    answer_entry.focus()

# функция проверки ответа
def check_answer():
    # получаем ответ пользователя
    answer = answer_entry.get().strip().lower()

    # получаем слово и перевод
    word = word_label.cget('text')
    translation = dictionary[word]

    # выбираем уровень сложности
    level = difficulty.get()

    # если уровень сложности 'Легко'
    if level == 'Легко':
        # получаем порядок букв в переводе, который был показан на экране
        shuffled_translation = translation_label.cget('text')

        # проверяем, что ответ пользователя совпадает с переводом и был введен в правильном порядке
        if answer == translation and set(answer) == set(shuffled_translation):
            score += 1  # увеличиваем счетчик очков на 1
        else:
            score -= 1  # уменьшаем счетчик очков на 1
    # если уровень сложности 'Сложно'
    elif level == 'Сложно':
        # проверяем, что ответ пользователя совпадает с переводом
        if answer == translation:
            score += 3  # увеличиваем счетчик очков на 3
        else:
            score -= 1  # уменьшаем счетчик очков на 1

    score_label.config(text='Очки: ' + str(score))  # отображаем счетчик очков на экране
    start_game()  # начинаем новую игру

# создаем окно программы
window = tk.Tk()
window.title('Репетитор по английскому')
window.geometry('400x300')

# создаем элементы интерфейса
difficulty_label = tk.Label(window, text='Уровень сложности:')
difficulty_label.pack()

difficulty = tk.StringVar()
difficulty.set('Легко')
difficulty_menu = tk.OptionMenu(window, difficulty, 'Легко', 'Сложно')
difficulty_menu.pack()

word_label = tk.Label(window, font=('Arial', 16), text='')
word_label.pack()

translation_label = tk.Label(window, font=('Arial', 16), text='')
translation_label.pack()

answer_label = tk.Label(window, text='Введите перевод:')
answer_label.pack()

answer_entry = tk.Entry(window)
answer_entry.pack()

check_button = tk.Button(window, text='Ответить', command=check_answer)
check_button.pack()

score_label = tk.Label(window, text='Очки: 10')
score_label.pack()

result_label = tk.Label(window, font=('Arial', 16), text='')
result_label.pack()

# список слов для перевода
words_list = list(dictionary.keys())

start_game()  #начинаем игру

window.mainloop()