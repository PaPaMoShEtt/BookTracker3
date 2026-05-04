import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Training Planner")
        self.geometry("600x400")
        self.create_widgets()
        self.data = []

    def create_widgets(self):
        # Поля ввода
        ttk.Label(self, text="Дата:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Тип:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Entry(self)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Длительность:").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = ttk.Entry(self)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        ttk.Button(self, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self, columns=("date", "type", "duration"), show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("duration", text="Длительность")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def add_training(self):
        date = self.date_entry.get()
        type_ = self.type_entry.get()
        duration = self.duration_entry.get()

        # Валидация
        try:
            datetime.strptime(date, "%d.%m.%Y")
            duration = float(duration)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный ввод данных!")
            return

        self.tree.insert("", "end", values=(date, type_, duration))
        self.data.append({"date": date, "type": type_, "duration": duration})

    def save_to_json(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_from_json(self):
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
                self.tree.delete(*self.tree.get_children())
                for item in self.data:
                    self.tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))
        except FileNotFoundError:
            messagebox.showinfo("Информация", "Файл не найден.")

# Запуск приложения
if __name__ == "__main__":
    app = TrainingPlanner()
    app.mainloop()