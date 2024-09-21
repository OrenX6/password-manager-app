import json  # built-in package
import random
from tkinter import *  # import everything - only classes and constants, not modules !
from tkinter import messagebox  # module

import pyperclip

FONT = ("Arial", 12, "bold")
GREEN = "#9bdeac"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    """
    Generate a random password at the password box.
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
               'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    random_letters = random.choices(letters, k=random.randint(8, 10))
    random_symbols = random.choices(symbols, k=random.randint(2, 4))
    random_numbers = random.choices(numbers, k=random.randint(2, 4))

    password = random_letters + random_symbols + random_numbers  # list object

    random.shuffle(password)
    password = "".join(password)

    if password_box.get():
        password_box.delete(0, END)

    password_box.insert(0, password)
    pyperclip.copy(password)  # The text to be copied to the clipboard.


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    """
    Save the data in a text file, If the website name is already exits in our saved data
    change only its password .
    """
    website = website_box.get().strip()
    email = email_username_box.get().strip()
    password = password_box.get().strip()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if website == "" or email == "" or not password:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            # error if the file does not exist
            with open(file="data.json", mode="r") as data_file:  # must be readable !
                # reading the old data
                data = json.load(data_file)  # Dict object

        # json file doesn't exist or There is no data in json file (empty)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as error_message:
            data = new_data
            print(error_message)
        else:
            # updating the old data with new data
            data.update(new_data)  # Dict method

        with open(file="data.json", mode="w") as data_file:  # must be writable
            json.dump(data, data_file, indent=4)

        website_box.delete(0, END)
        password_box.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website_name = website_box.get()  # String name or None
    try:
        with open(file="data.json", mode="r") as data_file:
            data = json.load(data_file)  # Dict object

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")

    except json.decoder.JSONDecodeError:
        messagebox.showinfo(title="File empty", message="No Data in this file, please add Data")

    else:
        if website_name in data:
            email = data[website_name]["email"]
            password = data[website_name]["password"]
            info = f"Email: {email}\n\nPassword: {password}"
            messagebox.showinfo(title=website_name, message=info)
        else:
            messagebox.showinfo(message=f"No details for {website_name} exists")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()  # default size is 1080 x 1920
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(window, height=200, width=200)  # Canvas windget
logo = PhotoImage(file="logo.png")  # PhotoImage object

canvas.create_image(100, 100, image=logo)  # create an image item inside the canvas
canvas.grid(row=0, column=1)

# Labels:
website_label = Label(window, text="Website:", font=FONT)
website_label.grid(row=1, column=0)

email_username_label = Label(window, text="Email/Username:", font=FONT)
email_username_label.grid(row=2, column=0)

password_label = Label(window, text="Password:", font=FONT)
password_label.grid(row=3, column=0)

# Entries:
website_box = Entry(window, font=FONT)
website_box.grid(row=1, column=1, columnspan=2, sticky="EW")  # spans across 2 columns
website_box.focus()

email_username_box = Entry(window, font=FONT)
email_username_box.grid(row=2, column=1, columnspan=2, sticky="EW")  # spans across 2 columns
email_username_box.insert(END, string="owenbech@gmail.com")

password_box = Entry(window, font=FONT)
password_box.grid(row=3, column=1, sticky="EW")  # stretches the widget left and right

# Buttons:
search_button = Button(window, text="Search", bg=GREEN, command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

generate_button = Button(window, text="Generate Password", bg=GREEN, command=generate_password)
generate_button.grid(row=3, column=2, sticky="EW")

add_button = Button(window, text="Add", bg=GREEN, command=save_data)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")  # stick the widget to the right and left edge

window.mainloop()
