import json
import sys
import tkinter as tk
import tkinter.filedialog
import subprocess
from time import sleep
from tkinter import W, N, E, S


class HiitTraining(tk.Frame):
    def __init__(self, title="HIIT Training", master=None):
        self.tasks = []
        self.running_tasks = []
        tk.Frame.__init__(self, master)
        self.master.geometry("900x400+10+10")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky=S + N + W + E)
        self.create_widgets()
        self.master.title(title)
        self.original_title = title
        self.running = False

    def create_widgets(self):
        label_config = {'sticky': W + N + E + S,
                        'padx': 20,
                        'ipady': 5}
        button_config = {'pady': 15}
        self.task_name_label = tk.Label(self,
                                        text="Task name",
                                        fg="light green",
                                        bg="dark green",
                                        font="Helvetica 45 bold italic")
        self.count_down_label = tk.Label(self,
                                         text="",
                                         fg="red",
                                         bg="yellow",
                                         font="Helvetica 40 bold italic")

        self.next_task_label = tk.Label(self,
                                        text="",
                                        font="Helvetica 20 italic")
        self.start_button = tk.Button(self, text="Start",
                                      width=40,
                                      font="Helvetica 16 bold italic",
                                      command=self.start)

        self.load_tasks_button = tk.Button(self, text="Open tasks file",
                                           width=40,
                                           font="Helvetica 16 bold italic",
                                           command=self.open_tasks_file)

        self.task_name_label.grid(row=0, column=0, columnspan=2, sticky=S + N + W + E)
        self.count_down_label.grid(row=1, column=0, columnspan=2, sticky=S + N + W + E)
        self.next_task_label.grid(row=2, column=0, columnspan=2, sticky=S + N + W + E)
        self.start_button.grid(row=3, column=0, padx=10, pady=15)
        self.load_tasks_button.grid(row=3, column=1, padx=10, pady=15)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def open_tasks_file(self):
        self.running_tasks = []
        self.tasks = json.load(tk.filedialog.askopenfile())['tasks']
        self.master.title(self.original_title)
        self.task_name_label.config(text="Total time: %s" % self.get_total_sec())
        self.count_down_label.config(text="%i tasks" % len(self.tasks))

    def get_total_sec(self):
        total = sum(t['duration'] for t in self.tasks)
        return "%i min %i sec" % (total / 60, total % 60)

    def do_tasks(self):
        if not self.running:
            return
        if not self.running_tasks:
            self.training_finished()
            return

        task = self.running_tasks[0]
        if task['duration'] >= 0:
            self.task_name_label.config(text=task['name'])
            self.count_down_label.config(text="%i sec" % task['duration'])
            task['duration'] -= 1
            if task['duration'] < 5:
                self.show_next_task()
            self.after(1000, self.do_tasks)
        else:
            self.running_tasks.pop(0)
            if self.running_tasks:
                self.say_it(self.running_tasks[0]['name'])
                self.master.title(self.original_title + " - Running (%i remains)" % len(self.running_tasks))
            self.hide_next_task()
            self.do_tasks()

    def show_next_task(self):
        if len(self.running_tasks) > 1:
            self.next_task_label.config(text="Next - %s" % self.running_tasks[1]['name'])
        else:
            self.next_task_label.config(text="THIS IS THE LAST TASK!!! KEEP GOING!")

    def say_it(self, word):
        subprocess.call("echo '%s' | festival --tts" % word, shell=True)

    def hide_next_task(self):
        self.next_task_label.config(text="")

    def training_finished(self):
        self.task_name_label.config(text="You are awesome!!!")
        self.count_down_label.config(text="")
        self.stop()

    def start(self):
        self.master.title(self.original_title + " - Running")
        self.start_button.config(text="Stop",
                                 command=self.stop)
        if not self.running_tasks:
            self.running_tasks = self.tasks
        self.say_it(self.running_tasks[0]['name'])
        self.running = True
        self.do_tasks()

    def stop(self):
        self.master.title(self.original_title + " - Stopped")
        self.start_button.config(text="Start",
                                 command=self.start)
        self.running = False


if __name__ == '__main__':
    app = HiitTraining()
    app.mainloop()
