import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class PhonebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Book Application")
        self.root.geometry("700x550")
        self.root.configure(bg='#f0f0f0')
        
        # Database file
        self.db_file = "contacts.json"
        self.load_contacts()
        
        # Default categories
        self.categories = ["Work", "Personal", "Family", "Friends", "Other"]
        
        # Setup UI
        self.setup_ui()
    
    def load_contacts(self):
        """Load contacts from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    self.contacts = json.load(f)
            except:
                self.contacts = {}
        else:
            self.contacts = {}
    
    def save_contacts(self):
        """Save contacts to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.contacts, f, indent=2)
    
    def setup_ui(self):
        """Create the user interface"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="📞 Phone Book", 
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=10)
        
        # Input Frame
        input_frame = tk.LabelFrame(
            self.root, 
            text="Add/Edit Contact",
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        input_frame.pack(padx=10, pady=10, fill="x")
        
        # Name field
        tk.Label(input_frame, text="Name:", bg='#f0f0f0', font=("Arial", 10)).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Phone field
        tk.Label(input_frame, text="Phone:", bg='#f0f0f0', font=("Arial", 10)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.phone_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Email field
        tk.Label(input_frame, text="Email:", bg='#f0f0f0', font=("Arial", 10)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.email_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Category field
        tk.Label(input_frame, text="Category:", bg='#f0f0f0', font=("Arial", 10)).grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.category_var = tk.StringVar(value="Personal")
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=self.categories, width=27, state="readonly", font=("Arial", 10))
        self.category_combo.grid(row=3, column=1, padx=5, pady=5)
        
        # Button Frame
        button_frame = tk.Frame(input_frame, bg='#f0f0f0')
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Button(
            button_frame, 
            text="Add Contact", 
            command=self.add_contact,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 10),
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, 
            text="Clear", 
            command=self.clear_fields,
            bg='#FFC107',
            fg='white',
            font=("Arial", 10),
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Search Frame
        search_frame = tk.Frame(self.root, bg='#f0f0f0')
        search_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0', font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30, font=("Arial", 10))
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_contacts())
        
        # Filter Frame
        filter_frame = tk.Frame(self.root, bg='#f0f0f0')
        filter_frame.pack(padx=10, pady=5, fill="x")
        
        tk.Label(filter_frame, text="Filter by Category:", bg='#f0f0f0', font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=["All"] + self.categories, width=20, state="readonly", font=("Arial", 10))
        filter_combo.pack(side=tk.LEFT, padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_list())
        
        # Contacts List Frame
        list_frame = tk.LabelFrame(
            self.root,
            text="Contacts",
            font=("Arial", 10, "bold"),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Treeview for displaying contacts
        columns = ('Name', 'Phone', 'Email', 'Category')
        self.tree = ttk.Treeview(list_frame, columns=columns, height=10, show='headings')
        
        self.tree.column('Name', width=120)
        self.tree.column('Phone', width=120)
        self.tree.column('Email', width=180)
        self.tree.column('Category', width=100)
        
        self.tree.heading('Name', text='Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Category', text='Category')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Actions Frame
        actions_frame = tk.Frame(self.root, bg='#f0f0f0')
        actions_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Button(
            actions_frame,
            text="Edit Selected",
            command=self.edit_contact,
            bg='#2196F3',
            fg='white',
            font=("Arial", 10),
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            actions_frame,
            text="Delete Selected",
            command=self.delete_contact,
            bg='#f44336',
            fg='white',
            font=("Arial", 10),
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            actions_frame,
            text="Refresh",
            command=self.refresh_list,
            bg='#FF9800',
            fg='white',
            font=("Arial", 10),
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Load contacts into the list
        self.refresh_list()
        
        # Bind double-click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_contact())
    
    def add_contact(self):
        """Add a new contact"""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        category = self.category_var.get()
        
        if not name:
            messagebox.showwarning("Error", "Name cannot be empty!")
            return
        
        if not phone:
            messagebox.showwarning("Error", "Phone cannot be empty!")
            return
        
        if not phone.isdigit() or len(phone) < 7:
            messagebox.showwarning("Error", "Please enter a valid phone number!")
            return
        
        if name in self.contacts:
            messagebox.showwarning("Error", "Contact already exists!")
            return
        
        self.contacts[name] = {
            'phone': phone,
            'email': email,
            'category': category,
            'created': datetime.now().isoformat()
        }
        
        self.save_contacts()
        self.clear_fields()
        self.refresh_list()
        messagebox.showinfo("Success", f"Contact '{name}' added to {category}!")
    
    def edit_contact(self):
        """Edit selected contact"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Please select a contact to edit!")
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        name = values[0]
        
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        
        self.name_entry.insert(0, name)
        self.phone_entry.insert(0, self.contacts[name]['phone'])
        self.email_entry.insert(0, self.contacts[name]['email'])
        self.category_var.set(self.contacts[name].get('category', 'Personal'))
        
        # Delete old contact
        del self.contacts[name]
        self.tree.delete(item)
        self.save_contacts()
    
    def delete_contact(self):
        """Delete selected contact"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Please select a contact to delete!")
            return
        
        item = selected[0]
        name = self.tree.item(item)['values'][0]
        
        if messagebox.askyesno("Confirm", f"Delete '{name}'?"):
            del self.contacts[name]
            self.save_contacts()
            self.refresh_list()
            messagebox.showinfo("Success", "Contact deleted!")
    
    def search_contacts(self):
        """Search contacts in real-time"""
        query = self.search_entry.get().lower()
        filter_category = self.filter_var.get()
        
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search and display
        for name, data in self.contacts.items():
            category = data.get('category', 'Other')
            category_match = (filter_category == "All" or filter_category == category)
            
            if category_match and (query in name.lower() or query in data['phone'] or query in data['email'].lower()):
                self.tree.insert('', 'end', values=(name, data['phone'], data['email'], category))
    
    def refresh_list(self):
        """Refresh the contacts list"""
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filter_category = self.filter_var.get()
        
        # Load all contacts
        for name in sorted(self.contacts.keys()):
            data = self.contacts[name]
            category = data.get('category', 'Other')
            
            if filter_category == "All" or filter_category == category:
                self.tree.insert('', 'end', values=(name, data['phone'], data['email'], category))
    
    def clear_fields(self):
        """Clear input fields"""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.category_var.set("Personal")
        self.search_entry.delete(0, tk.END)
        self.filter_var.set("All")
        self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhonebookApp(root)
    root.mainloop()
