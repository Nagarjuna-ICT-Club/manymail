from tkinter import Tk
from gui import EmailApp

def main():
    root = Tk()
    app = EmailApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
