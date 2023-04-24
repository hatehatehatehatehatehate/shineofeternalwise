import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from img import images_base64
import base64
from io import BytesIO
from questions import questions_data


class IQTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IQ Test")
        self.geometry("800x600")
        self.questions = self.load_questions()
        self.current_question = 0
        self.points = 0

        self.create_widgets()

    def load_questions(self):
        return questions_data


    # The rest of the methods go here


    def create_widgets(self):
        self.question_label = ttk.Label(
            self, text=self.questions[self.current_question]["text"], wraplength=300)
        self.question_label.grid(column=0, row=0, padx=20, pady=20)

        image_data = base64.b64decode(images_base64[self.current_question])
        self.image = Image.open(BytesIO(image_data))
        self.image = self.image.resize((300, 300), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = ttk.Label(self, image=self.photo)
        self.image_label.grid(column=1, row=0, padx=20, pady=20)

        self.choice_var = tk.StringVar()
        for i, choice in enumerate(self.questions[self.current_question]["choices"]):
            radio = ttk.Radiobutton(
                self, text=choice, variable=self.choice_var, value=choice)
            radio.grid(column=0, row=i + 1, padx=20, pady=5, sticky="w")

        self.submit_button = ttk.Button(
            self, text="Submit", command=self.submit_answer)
        self.submit_button.grid(column=0, row=5, padx=20, pady=20)

    def submit_answer(self):
        selected_choice = self.choice_var.get()
        if selected_choice == self.questions[self.current_question]["answer"]:
            self.points += 1

        self.current_question += 1

        if self.current_question < len(self.questions):
            self.question_label.configure(text=self.questions[self.current_question]["text"])
            image_data = base64.b64decode(images_base64[self.current_question])
            self.image = Image.open(BytesIO(image_data))
            self.image = self.image.resize((300, 300), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.configure(image=self.photo)

            # Reset the radio buttons to default (unselected) state
            self.choice_var.set("")

            for i, choice in enumerate(self.questions[self.current_question]["choices"]):
                radio = ttk.Radiobutton(self, text=choice, variable=self.choice_var, value=choice)
                radio.grid(column=0, row=i + 1, padx=20, pady=5, sticky="w")
        else:
            self.show_results()


    def show_results(self):
        iq = self.points_to_iq(self.points)

        for widget in self.grid_slaves():
            widget.destroy()

        result_label = ttk.Label(
            self, text=f"Your IQ: {iq}", font=("Helvetica", 24))
        result_label.grid(column=0, row=0, padx=20, pady=20)

        restart_button = ttk.Button(
            self, text="Restart", command=self.restart_test)
        restart_button.grid(column=0, row=1, padx=20, pady=20)

    def points_to_iq(self, points):
        max_points = len(self.questions)
        wrong_answers = max_points - points
        penalty = wrong_answers * 2  # Define a penalty value for each wrong answer

        iq = int((points / max_points) * 100) + 100 - penalty
        return iq


    def restart_test(self):
        self.current_question = 0
        self.points = 0
        self.create_widgets()


if __name__ == "__main__":
    app = IQTestApp()
    app.mainloop()
