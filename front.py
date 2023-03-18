import tkinter as tk

from PIL import ImageTk


class main:
    def __init__(self, root):
        self.root = root
        self.root.title("User Login")
        self.root.geometry("1920x1080")

        # BG IMAGE
        self.bg = ImageTk.PhotoImage(file="images/bg.jpg")
    # self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)


def redirect_to_page(selection):
    if selection == "Adhar Card":
        pass

    elif selection == "PAN Card":
        pass


options = ["Adhar Card", "PAN Card"]
var = tk.StringVar(value=options[0])
dropdown = tk.OptionMenu(root, var, *options, command=redirect_to_page)
dropdown.pack()

root = Tk()
root.mainloop()
