import tkinter as tk
from tkinter import messagebox

def insert_variable(template_text_widget, var_entry_widget):
    try:
        selected = template_text_widget.selection_get()
        start = template_text_widget.index(tk.SEL_FIRST)
        end = template_text_widget.index(tk.SEL_LAST)
        variable_name = var_entry_widget.get().strip()
        if not variable_name:
            raise Exception("Variable name is empty")

        template_text_widget.delete(start, end)
        template_text_widget.insert(start, f"{{{{{variable_name}}}}}")
    except tk.TclError:
        messagebox.showerror("Error", "Please select some text to turn into a variable.")
