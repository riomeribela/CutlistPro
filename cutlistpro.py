


import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
import os
from datetime import datetime

class CutlistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mill Room Cutlist Order App")
        
        # File to save and load cutlist
        self.cutlist_file = "cutlist.txt"

        # Initialize departments and cutlist
        self.departments = ['Mill Room', 'Floors', 'Cab Shop', 'Electrical', 'Plumbing', 'Partions', 'Ext Bottoms', 'Ext Tops', 'Roof Build', 'Roof Set', 'Carpet']  # Added 'Mill Room'
        self.cutlist = []

        # Set up the left frame with department buttons
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, padx=10)

        # Create department buttons on the left side
        self.department_buttons = {}
        for dept in self.departments:
            button = tk.Button(self.left_frame, text=dept, font=("Helvetica", 14),height=2, width=25, command=lambda dept=dept: self.show_department_items(dept) if dept != 'Mill Room' else self.show_mill_room())
            button.pack(pady=5)
            self.department_buttons[dept] = button

        # Set up the right frame with the cutlist display
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.LEFT, padx=10)

        # Add a label for the cutlist
        self.cutlist_label = tk.Label(self.right_frame, text="Cutlist", font=("Helvetica", 20))
        self.cutlist_label.pack(pady=10)

        # Listbox to display cutlist items
        self.cutlist_box = tk.Listbox(self.right_frame, height=30, width=85, font=("Helvetica", 14))
        self.cutlist_box.pack()

        # Scrollbar for the listbox
        self.scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=self.cutlist_box.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cutlist_box.config(yscrollcommand=self.scrollbar.set)

        # Set up the bottom frame with the save, load, and view log buttons
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.RIGHT, pady=10)

        # Create the save, load, and view log buttons (stacked vertically)
        self.save_button = tk.Button(self.bottom_frame, text="Save Cutlist", width=20, command=self.save_cutlist)
        self.save_button.pack(pady=5)  # Added padding for spacing
        
        self.load_button = tk.Button(self.bottom_frame, text="Load Cutlist", width=20, command=self.load_cutlist)
        self.load_button.pack(pady=5)  # Added padding for spacing

        # Add the View Log button
        self.view_log_button = tk.Button(self.bottom_frame, text="View Log", width=20, command=self.view_log)
        self.view_log_button.pack(pady=5)  # Added padding for spacing

        # Load the previous cutlist when the program starts
        self.load_cutlist()

    def add_to_cutlist(self, department, selected_items):
        for item in selected_items:
            item['department'] = department
            item['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cutlist.append(item)
        self.update_cutlist_display()
        self.save_cutlist()  # Automatically save the cutlist after adding an item

    def update_cutlist_display(self):
        self.cutlist_box.delete(0, tk.END)  # Clear current list
        for item in self.cutlist:
            self.cutlist_box.insert(
                tk.END, 
                f"{item['department']} | {item['name']} | {item['size']} | {item['material']} | Saw: {item['saw_type']} | Quantity: {item['quantity']} | Ordered: {item['timestamp']}"
            )

    def save_cutlist(self):
        try:
            with open(self.cutlist_file, 'w') as file:
                for item in self.cutlist:
                    file.write(f"{item['department']} | {item['name']} | {item['size']} | {item['material']} | {item['saw_type']} | {item['quantity']} | {item['timestamp']}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save cutlist: {e}")

    def load_cutlist(self):
        if os.path.exists(self.cutlist_file):
            try:
                with open(self.cutlist_file, 'r') as file:
                    loaded_items = file.readlines()
                    self.cutlist = []
                    for line in loaded_items:
                        parts = line.strip().split(" | ")
                        if len(parts) == 7:  # The format includes department, timestamp, and quantity
                            department, name, size, material, saw_type, quantity, timestamp = parts
                            self.cutlist.append({
                                'department': department, 'name': name, 'size': size, 'material': material, 'saw_type': saw_type, 'quantity': int(quantity), 'timestamp': timestamp
                            })
                self.update_cutlist_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load cutlist: {e}")
        else:
            print("No previous cutlist found. Starting with an empty list.")

    def show_department_items(self, department):
        department_items = {
            'Floors': [
                {'name': '37 1/2', 'size': '37 1/2x96', 'material': '5/8 OSB', 'saw_type': 'Gang'},
                {'name': '80', 'size': '80x48', 'material': '5/8 OSB', 'saw_type': 'Table'},
                {'name': '64', 'size': '64x48', 'material': '5/8 OSB', 'saw_type': 'Table'},
                {'name': '48', 'size': '48x48', 'material': '5/8 OSB', 'saw_type': 'Table'},
                {'name': '32', 'size': '32x48', 'material': '5/8 OSB', 'saw_type': 'Table'},
                {'name': '16 1/2', 'size': '16/12', 'material': '2x2', 'saw_type': 'Radial'},
                {'name': '5x5', 'size': '5x5', 'material': '7/16 OSB', 'saw_type': 'Radial'},
            ],
            'Cab Shop': [
                {'name': 'Frames', 'size': 'Large', 'material': '1x3', 'saw_type': 'Radial'},
                {'name': 'Frames', 'size': 'Medium', 'material': '1x3', 'saw_type': 'Radial'},
                {'name': 'Frames', 'size': 'Small', 'material': '1x3', 'saw_type': 'Radial'}
            ],
            'Electrical': [
                {'name': 'conduit', 'size': 'Angle cut in half', 'material': 'Conduit', 'saw_type': 'Radial'},
            ],
            'Roof Build': [
                {'name': '2x3 backer', 'size': '28 w/ 6x12 OSB', 'material': '2x3', 'saw_type': 'Radial'},
                {'name': '2x4x18', 'size': '18', 'material': '2x4', 'saw_type': 'Radial'},
                {'name': '2x4x40', 'size': '40', 'material': '2x4', 'saw_type': 'Radial'},
                {'name': 'Angles', 'size': 'ALL', 'material': '2x4', 'saw_type': 'Radial'},
                {'name': 'Facia', 'size': '145?', 'material': '1x6', 'saw_type': 'Radial'},
                {'name': '3', 'size': '3 x 96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': '3', 'size': '3 x 19', 'material': '7/16 OSB', 'saw_type': 'Radial'},
                {'name': '4 5/8', 'size': '4 5/8 x 96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': '5 3/4', 'size': '5 3/4 x 21', 'material': '7/16 OSB', 'saw_type': 'Radial'},
                {'name': '6 1/8', 'size': '6 1/8 x 96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': 'Dormer', 'size': '118 1/2', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': '22 1/2', 'size': '22 1/2', 'material': '2x3', 'saw_type': 'Radial'},
                {'name': '35 1/2', 'size': '35 1/2', 'material': '2x3', 'saw_type': 'Radial'},
            ],
            'Plumbing': [
                {'name': '16x11', 'size': '16x11', 'material': '7/16OSB,2x2', 'saw_type': 'Radial'},
            ],
            'Partions': [
                {'name': '44 1/4', 'size': '44 1/4', 'material': '2x6', 'saw_type': 'Radial'},
                {'name': '38 1/4', 'size': '38 1/4', 'material': '2x6', 'saw_type': 'Radial'},
                {'name': '32 1/2', 'size': '32 1/2', 'material': '2x6', 'saw_type': 'Radial'},
                {'name': '20 1/2', 'size': '20 1/2', 'material': '1x6', 'saw_type': 'Radial'},
                {'name': '2x3 32', 'size': '32', 'material': '2x3', 'saw_type': 'Radial'},
                {'name': '2x4 32', 'size': '32', 'material': '2x4', 'saw_type': 'Radial'},
            ],
            'Ext Bottoms': [
                {'name': '6 1/8', 'size': '6 1/8 x 96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': '7 7/8', 'size': '7 7/8 x 96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': '14', 'size': '14 x 96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': '22', 'size': '22 x 96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': '24', 'size': '24 x 96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': '32', 'size': '32 x 96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
            ],
            'Roof Set': [
                {'name': '21', 'size': '21x96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': '30', 'size': '30x96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': '39', 'size': '39x96', 'material': '7/16 OSB', 'saw_type': 'Gang'},
                {'name': 'Option A', 'size': '69 5/8, 9', 'material': '2x6', 'saw_type': 'Radial'},
                {'name': 'Option C', 'size': '69??', 'material': '2x6', 'saw_type': 'Radial'},
                {'name': 'Option D', 'size': '58 1/16, 3', 'material': '2x6', 'saw_type': 'Radial'},
                {'name': '1x2', 'size': '100', 'material': '1x2', 'saw_type': 'Radial'},
            ],
            'Ext Tops': [
                {'name': 'Soffit', 'size': '11 3/4', 'material': 'Soffit', 'saw_type': 'Radial'},
            ],
            'Carpet': [
                {'name': '1x2', 'size': '7', 'material': '1x2', 'saw_type': 'Radial'},
                {'name': 'Access Panels', 'size': '24x24', 'material': 'Gyp', 'saw_type': 'Table'},
                {'name': '3', 'size': '3x96', 'material': 'Gyp', 'saw_type': 'Table'},
            ],# Add other items here...
          
        }
        items = department_items.get(department, [])

        items_window = tk.Toplevel(self.root)
        items_window.title(f"{department} Items")

        selected_items = []
        for idx, item in enumerate(items):
            frame = tk.Frame(items_window)
            frame.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

            var = tk.IntVar()
            checkbox = tk.Checkbutton(frame, text=f"{item['name']} | {item['size']} | {item['material']} | {item['saw_type']}", variable=var, font=("Helvetica", 14)) 
            checkbox.pack(side=tk.LEFT, padx=5)

            quantity_var = tk.StringVar()
            quantity_entry = tk.Entry(frame, textvariable=quantity_var, width=5)
            quantity_entry.pack(side=tk.LEFT, padx=5)
            quantity_entry.insert(0, "1")

            selected_items.append({'var': var, 'quantity_var': quantity_var, 'item': item})

        def add_selected_items():
            items_to_add = []
            for entry in selected_items:
                if entry['var'].get() == 1:
                    quantity = entry['quantity_var'].get()
                    if not quantity.isdigit() or int(quantity) <= 0:
                        messagebox.showwarning("Invalid Quantity", f"Invalid quantity for {entry['item']['name']}. Skipping this item.")
                        continue
                    item = entry['item'].copy()
                    item['quantity'] = int(quantity)
                    items_to_add.append(item)

            if items_to_add:
                self.add_to_cutlist(department, items_to_add)
                items_window.destroy()
            else:
                messagebox.showwarning("No Items Selected", "Please select at least one item to add.")

        add_button = tk.Button(items_window, text="Add to Cutlist", command=add_selected_items)
        add_button.grid(row=len(items), column=0, pady=10)


    def show_mill_room(self):
        mill_room_window = tk.Toplevel(self.root)
        mill_room_window.title("Mill Room")
        mill_room_window.geometry("800x600")  # Set the window size

        # Main layout: Left frame for list, right frame for controls
        main_frame = tk.Frame(mill_room_window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas and scrollbar for the list (left side)
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Right frame for controls
        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Frames for Gang, Radial, and Table sections
        gang_frame = tk.Frame(scrollable_frame)
        gang_frame.pack(side=tk.TOP, padx=10, pady=10)

        radial_frame = tk.Frame(scrollable_frame)
        radial_frame.pack(side=tk.TOP, padx=10, pady=10)

        table_frame = tk.Frame(scrollable_frame)
        table_frame.pack(side=tk.TOP, padx=10, pady=10)

        tk.Label(gang_frame, text="Gang", font=("Helvetica", 14)).pack()
        tk.Label(radial_frame, text="Radial", font=("Helvetica", 14)).pack()
        tk.Label(table_frame, text="Table", font=("Helvetica", 14)).pack()

        # Dropdown for selecting team members in the right frame
        team_members = ["Mario Meribela", "David Eversole", "Laureano Santos", "Ben Bastock", "Kevin Rivas", "Louie Ortiz"]
        selected_team_member = tk.StringVar()
        selected_team_member.set(team_members[0])

        tk.Label(controls_frame, text="Select Team Member:", font=("Helvetica", 12)).pack(pady=5)
        team_member_dropdown = tk.OptionMenu(controls_frame, selected_team_member, *team_members)
        team_member_dropdown.pack(pady=5)

        # Variables for items
        gang_items = []
        radial_items = []
        table_items = []

        for item in self.cutlist:
            saw_type = item['saw_type']
            item_str = f"{item['name']} | {item['size']} | {item['material']} | Ordered: {item['quantity']}"
            var = tk.IntVar()
            quantity_made_var = tk.StringVar()

            if saw_type == 'Gang':
                gang_items.append((var, item, quantity_made_var))
                frame = tk.Frame(gang_frame)
            elif saw_type == 'Radial':
                radial_items.append((var, item, quantity_made_var))
                frame = tk.Frame(radial_frame)
            elif saw_type == 'Table':
                table_items.append((var, item, quantity_made_var))
                frame = tk.Frame(table_frame)

            frame.pack(anchor='w')
            checkbox = tk.Checkbutton(frame, text=item_str, variable=var, font=("Helvetica", 14))
            checkbox.pack(side=tk.LEFT, padx=5)
            quantity_entry = tk.Entry(frame, textvariable=quantity_made_var, width=5)
            quantity_entry.pack(side=tk.LEFT, padx=5)
            quantity_entry.insert(0, "0")

        # Button to complete selected items in the right frame
        def complete_selected_items():
            completed_items = []
            remaining_items = []
            for var, item, quantity_made_var in gang_items + radial_items + table_items:
                if var.get() == 1:
                    try:
                        quantity_made = int(quantity_made_var.get())
                        if quantity_made < 0:
                            raise ValueError("Quantity made cannot be negative.")
                        if quantity_made < item['quantity']:
                            remaining_item = item.copy()
                            remaining_item['quantity'] = item['quantity'] - quantity_made
                            remaining_items.append(remaining_item)

                        completed_items.append({
                            'department': item['department'],
                            'name': item['name'],
                            'size': item['size'],
                            'material': item['material'],
                            'saw_type': item['saw_type'],
                            'quantity_ordered': item['quantity'],
                            'quantity_made': quantity_made,
                            'team_member': selected_team_member.get(),
                            'ordered_timestamp': item['timestamp'],
                            'completed_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                    except ValueError:
                        messagebox.showwarning("Invalid Quantity", f"Invalid quantity made for {item['name']}. Skipping this item.")
                        continue

            self.cutlist = [item for item in self.cutlist if item not in [i[1] for i in gang_items + radial_items + table_items if i[0].get() == 1]]
            self.cutlist.extend(remaining_items)
            self.update_cutlist_display()

            if completed_items:
                with open("completion_log.txt", 'a') as log_file:
                    for item in completed_items:
                        log_file.write(f"{item['department']} | {item['name']} | {item['size']} | {item['material']} | {item['saw_type']} | Ordered: {item['quantity_ordered']} | Made: {item['quantity_made']} | Completed By: {item['team_member']} | Ordered: {item['ordered_timestamp']} | Completed: {item['completed_timestamp']}\n\n")
                messagebox.showinfo("Completion Log", "Selected items have been completed and logged.")
                self.save_cutlist()
                mill_room_window.destroy()
            else:
                messagebox.showwarning("No Items Selected", "Please select at least one item to complete.")

        complete_button = tk.Button(controls_frame, text="Complete Selected Items", command=complete_selected_items, font=("Helvetica", 12))
        complete_button.pack(pady=20)

   
    def view_log(self):
        # Create a new window to display the completion log
        log_window = tk.Toplevel(self.root)
        log_window.title("Completion Log")

        # Create a text widget to display the log
        log_text = tk.Text(log_window, wrap=tk.WORD, height=20, width=100)
        log_text.pack(padx=10, pady=10)

        # Load the completion log from the file
        try:
            with open("completion_log.txt", 'r') as log_file:
                log_contents = log_file.read()
                log_text.insert(tk.END, log_contents)  # Insert the log contents into the text widget
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load log: {e}")

        # Add a scrollbar to the text widget
        scrollbar = tk.Scrollbar(log_window, command=log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        log_text.config(yscrollcommand=scrollbar.set)

        # Function to clear the log
        def clear_log():
            password = simpledialog.askstring("Password", "Enter password to clear log:")
            if password == '1379':
                open("completion_log.txt", 'w').close()  # Clear the log file
                log_text.delete(1.0, tk.END)  # Clear the text widget
                messagebox.showinfo("Success", "Log cleared successfully.")
            else:
                messagebox.showerror("Error", "Incorrect password.")

        # Function to archive the log
        def archive_log():
            password = simpledialog.askstring("Password", "Enter password to Archive log:")
            if password == '1379':
            
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Create a timestamp
                archive_filename = f"CutListArchive{timestamp}.txt"
                try:
                    with open(archive_filename, 'w') as archive_file:
                        archive_file.write(log_text.get(1.0, tk.END))  # Save current log to archive
                    open("completion_log.txt", 'w').close()  # Clear the log file
                    log_text.delete(1.0, tk.END)  # Clear the text widget
                    messagebox.showinfo("Success", f"Log archived to {archive_filename}.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to archive log: {e}")

        # Add Clear Log button
        clear_log_button = tk.Button(log_window, text="Clear Log", command=clear_log)
        clear_log_button.pack(pady=5)

        # Add Archive button
        archive_button = tk.Button(log_window, text="Archive", command=archive_log)
        archive_button.pack(pady=5)


# Create the main window
root = tk.Tk()
app = CutlistApp(root)
root.mainloop()









