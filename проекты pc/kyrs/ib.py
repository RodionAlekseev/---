import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


class CaesarCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифр Цезаря")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        try:
            self.root.iconbitmap("caesar.ico")
        except:
            pass

        self.shift_var = tk.IntVar(value=3)
        self.language_var = tk.StringVar(value="ru")
        self.keep_case_var = tk.BooleanVar(value=True)
        self.keep_spaces_var = tk.BooleanVar(value=True)

        self.setup_ui()

    def setup_ui(self):
        self.create_menu()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        self.cipher_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cipher_tab, text='Шифрование')

        self.create_cipher_tab()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Создать", command=self.new_file)
        file_menu.add_command(label="Открыть...", command=self.open_file)
        file_menu.add_command(label="Сохранить как...", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Копировать результат", command=self.copy_result)
        edit_menu.add_command(label="Вставить текст", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Очистить все", command=self.clear_all)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def create_cipher_tab(self):
        settings_frame = ttk.LabelFrame(self.cipher_tab, text="Настройки шифрования", padding=10)
        settings_frame.pack(fill='x', padx=10, pady=(10, 5))

        ttk.Label(settings_frame, text="Ключ (сдвиг):").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.shift_spinbox = ttk.Spinbox(settings_frame, from_=1, to=100, width=10, textvariable=self.shift_var)
        self.shift_spinbox.grid(row=0, column=1, sticky='w', padx=(0, 20))

        ttk.Label(settings_frame, text="Язык:").grid(row=0, column=2, sticky='w', padx=(0, 5))
        self.lang_combobox = ttk.Combobox(settings_frame, textvariable=self.language_var, values=["ru", "en"], state="readonly", width=10)
        self.lang_combobox.grid(row=0, column=3, sticky='w', padx=(0, 20))

        ttk.Checkbutton(settings_frame, text="Сохранять регистр", variable=self.keep_case_var).grid(row=0, column=4,padx=(0, 10))
        ttk.Checkbutton(settings_frame, text="Сохранять пробелы и знаки препинания", variable=self.keep_spaces_var).grid(row=0, column=5)

        input_frame = ttk.LabelFrame(self.cipher_tab, text="Исходный текст", padding=10)
        input_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=8, font=('Arial', 10))
        self.input_text.pack(fill='both', expand=True)

        button_frame = ttk.Frame(self.cipher_tab)
        button_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(button_frame, text="Зашифровать", command=self.encrypt, style="Accent.TButton").pack(side='left',padx=(0, 10))
        ttk.Button(button_frame, text="Расшифровать", command=self.decrypt, style="Accent.TButton").pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="Очистить", command=self.clear_input).pack(side='left')

        result_frame = ttk.LabelFrame(self.cipher_tab, text="Результат", padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=(5, 10))

        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=8, font=('Arial', 10),state='disabled')
        self.result_text.pack(fill='both', expand=True)

        result_buttons_frame = ttk.Frame(result_frame)
        result_buttons_frame.pack(fill='x', pady=(5, 0))

        ttk.Button(result_buttons_frame, text="Копировать результат", command=self.copy_result).pack(side='left')
        ttk.Button(result_buttons_frame, text="Поменять местами", command=self.swap_texts).pack(side='left',padx=(10, 0))

    def get_alphabet(self):
        if self.language_var.get() == "ru":
            return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        else:
            return 'abcdefghijklmnopqrstuvwxyz'

    def caesar_cipher(self, text, shift, encrypt=True):
        if not text:
            return ""

        alphabet = self.get_alphabet()
        result = []

        for char in text:
            original_char = char
            char_lower = char.lower()

            if char_lower not in alphabet and self.keep_spaces_var.get():
                result.append(char)
                continue
            elif char_lower not in alphabet:
                continue

            idx = alphabet.find(char_lower)

            if encrypt:
                new_idx = (idx + shift) % len(alphabet)
            else:
                new_idx = (idx - shift) % len(alphabet)

            new_char = alphabet[new_idx]
            if self.keep_case_var.get() and original_char.isupper():
                new_char = new_char.upper()

            result.append(new_char)

        return ''.join(result)

    def encrypt(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст для шифрования!")
            return

        try:
            shift = int(self.shift_var.get())
            encrypted = self.caesar_cipher(text, shift, encrypt=True)

            self.result_text.configure(state='normal')
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", encrypted)
            self.result_text.configure(state='disabled')

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при шифровании: {str(e)}")

    def decrypt(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст для дешифрования!")
            return

        try:
            shift = int(self.shift_var.get())
            decrypted = self.caesar_cipher(text, shift, encrypt=False)

            self.result_text.configure(state='normal')
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", decrypted)
            self.result_text.configure(state='disabled')

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при дешифровании: {str(e)}")

    def copy_result(self):
        try:
            result = self.result_text.get("1.0", tk.END).strip()
            if result:
                self.root.clipboard_clear()
                self.root.clipboard_append(result)
                messagebox.showinfo("Успех", "Результат скопирован в буфер обмена!")
            else:
                messagebox.showwarning("Предупреждение", "Нет результата для копирования!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при копировании: {str(e)}")

    def paste_text(self):
        try:
            text = self.root.clipboard_get()
            if text:
                self.input_text.insert(tk.END, text)
        except:
            messagebox.showwarning("Предупреждение", "Не удалось вставить текст!")

    def clear_input(self):
        self.input_text.delete("1.0", tk.END)

    def clear_result(self):
        self.result_text.configure(state='normal')
        self.result_text.delete("1.0", tk.END)
        self.result_text.configure(state='disabled')

    def clear_all(self):
        self.clear_input()
        self.clear_result()

    def swap_texts(self):
        result = self.result_text.get("1.0", tk.END).strip()
        if result:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", result)
            self.clear_result()

    def new_file(self):
        if self.input_text.get("1.0", "end-1c"):
            if messagebox.askyesno("Подтверждение", "Текущий текст будет удален. Продолжить?"):
                self.clear_all()
        else:
            self.clear_all()

    def open_file(self):
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )

        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()

                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", text)

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {str(e)}")

    def save_file(self):
        from tkinter import filedialog
        result = self.result_text.get("1.0", tk.END).strip()

        if not result:
            messagebox.showwarning("Предупреждение", "Нет результата для сохранения!")
            return

        filepath = filedialog.asksaveasfilename(
            title="Сохранить как",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )

        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(result)
                messagebox.showinfo("Успех", f"Файл сохранен: {filepath}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def show_about(self):
        about_text = """Шифр Цезаря 

Программа для шифрования и дешифрования текста
методом шифра Цезаря.

Выполнил:
Студент группы ПИб-21
Алексеев Р.Р.
Вариант: 3"""

        messagebox.showinfo("О программе", about_text)


def main():
    root = tk.Tk()

    try:
        import ttkthemes
        style = ttkthemes.ThemedStyle(root)
        style.set_theme("arc")
    except ImportError:
        pass

    app = CaesarCipherApp(root)

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()