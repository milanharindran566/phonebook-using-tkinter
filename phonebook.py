import tkinter as tk
from tkinter import messagebox, Scrollbar, StringVar, Text

# Helper functions
def setup_search_edit_frame(parent):
    search_frame = tk.Toplevel(parent)
    search_frame.title("Search/Edit")
    search_frame.configure(bg='lightyellow')
    
    tk.Label(search_frame, text="Search", bg='lightyellow').pack()
    tk.Entry(search_frame, textvariable=search).pack()
    
    tk.Label(search_frame, text="Edit (replace found text)", bg='lightyellow').pack()
    tk.Entry(search_frame, textvariable=edits).pack()
    
    tk.Button(search_frame, text="Search", command=search_entry).pack(pady=2)
    tk.Button(search_frame, text="Edit", command=edit_entry).pack(pady=2)
    tk.Button(search_frame, text="Clear", command=clear_search).pack(pady=2)
    
    global search_results
    search_results = Text(search_frame, height=10, width=70)
    search_results.pack()
    
    return search_frame

def add_entry():
    first = fname.get()
    last = lname.get()
    phone_number = phone.get()
    email_addr = email.get()

    if not (first and last and phone_number and email_addr):
        messagebox.showwarning("Missing Info", "Please fill out all fields.")
        return
    
    if not email_addr.endswith(".com"):
        messagebox.showwarning("Invalid Email", "Please use a valid .com email.")
        return
    
    if not phone_number.isdigit():
        messagebox.showwarning("Invalid Phone Number", "Please use digits only.")
        return
    
    if len(phone_number) != 10:
        messagebox.showwarning("Invalid Phone Number", "Please use a 10-digit number.")
        return

    entry = f"{first}\t{last}\t{phone_number}\t{email_addr}\n"
    display_text.insert(tk.END, entry)

    with open("phone.txt", "a") as f:
        f.write(entry)

    reset_entry()

def reset_entry():
    fname.set("")
    lname.set("")
    phone.set("")
    email.set("")

def clear_display():
    display_text.delete(1.0, tk.END)

def clear_search():
    search_results.delete(1.0, tk.END)

def search_entry():
    keyword = search.get()
    found = False
    search_results.delete(1.0, tk.END)

    with open("phone.txt", "r") as f:
        for line in f:
            if keyword in line:
                search_results.insert(tk.END, line)
                found = True

    if not found:
        messagebox.showinfo("Search", "No matching entry found.")

def edit_entry():
    original = search.get()
    new_value = edits.get()

    updated_lines = []
    found = False

    with open("phone.txt", "r") as f:
        for line in f:
            if original in line:
                line = line.replace(original, new_value)
                found = True
            updated_lines.append(line)

    if found:
        with open("phone.txt", "w") as f:
            f.writelines(updated_lines)

        messagebox.showinfo("Edit", "Edit successful.")
        search_results.delete(1.0, tk.END)
        for line in updated_lines:
            search_results.insert(tk.END, line)
    else:
        messagebox.showinfo("Edit", "Original text not found.")

    search.set("")
    edits.set("")

# Create main window
root = tk.Tk()
root.title("Phonebook")
root.configure(bg='lightblue')

# Variables
fname = StringVar()
lname = StringVar()
phone = StringVar()
email = StringVar()
search = StringVar()
edits = StringVar()

# Layout Frames
form_frame = tk.Frame(root, bg='lightblue', pady=10)
form_frame.pack()

buttons_frame = tk.Frame(root, bg='lightblue', pady=5)
buttons_frame.pack()

display_frame = tk.Frame(root)
display_frame.pack()

# Add Search/Edit button to buttons_frame
tk.Button(buttons_frame, text="Search/Edit", command=lambda: setup_search_edit_frame(root)).grid(row=0, column=4, padx=5)

# Form Inputs
fields = [("First Name", fname), ("Last Name", lname), ("Phone", phone), ("Email", email)]
for i, (label_text, var) in enumerate(fields):
    tk.Label(form_frame, text=label_text, bg='lightblue').grid(row=i, column=0, sticky='e', padx=5, pady=2)
    tk.Entry(form_frame, textvariable=var, width=30).grid(row=i, column=1, pady=2)

# Buttons
tk.Button(buttons_frame, text="Add Entry", command=add_entry).grid(row=0, column=0, padx=5)
tk.Button(buttons_frame, text="Reset", command=reset_entry).grid(row=0, column=1, padx=5)
tk.Button(buttons_frame, text="Clear Display", command=clear_display).grid(row=0, column=2, padx=5)
tk.Button(buttons_frame, text="Quit", command=root.quit).grid(row=0, column=3, padx=5)

# Display Box
display_text = Text(display_frame, height=15, width=80)
display_text.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar = Scrollbar(display_frame, command=display_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
display_text.config(yscrollcommand=scrollbar.set)
display_text.insert(tk.END, "First Name\tLast Name\tPhone\tEmail\n")
display_text.insert(tk.END, "-"*80 + "\n")

tk.Button(buttons_frame, text="Search/Edit", command=lambda: setup_search_edit_frame(root)).grid(row=0, column=4, padx=5)

# Start the GUI loop
root.mainloop()
