import os
import shutil
import sys
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def select_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

def select_target():
    target_path = filedialog.askdirectory()
    target_entry.delete(0, tk.END)
    target_entry.insert(0, target_path)

def create_symbolic_link():
    origin_folder = folder_entry.get()
    target_folder = target_entry.get()
    
    try:
        folder_name = os.path.basename(origin_folder)
        target_origin_path = os.path.join(target_folder, folder_name)
        
        # Move the original folder to the target directory
        shutil.move(origin_folder, target_origin_path)
        
        # Create a symbolic link in the original folder's location
        os.symlink(target_origin_path, origin_folder)
        
        status_text.insert(tk.END, "Symbolic link created and origin folder moved successfully.\n")
        status_text.see(tk.END)  # Scroll to the end
    except Exception as e:
        status_text.insert(tk.END, f"Error: {str(e)}\n", "error")
        status_text.see(tk.END)  # Scroll to the end

# Check if running as admin, if not, prompt to restart as admin
if not is_admin():
    messagebox.showinfo("Admin Permission Required", "This program requires administrative privileges. Please restart the program as an administrator.")
    sys.exit()

# Create the main window
root = tk.Tk()
root.title("Symbolic Link Creator")

# Create and position widgets
folder_frame = tk.Frame(root)
folder_frame.pack(fill=tk.X, padx=10, pady=10)

folder_label = tk.Label(folder_frame, text="Select Origin Folder:")
folder_label.pack(side=tk.LEFT, padx=(0, 5))

folder_entry = tk.Entry(folder_frame)
folder_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

folder_button = tk.Button(folder_frame, text="Browse", command=select_folder)
folder_button.pack(side=tk.LEFT, padx=(5, 0))

target_frame = tk.Frame(root)
target_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

target_label = tk.Label(target_frame, text="Select Target Folder:")
target_label.pack(side=tk.LEFT, padx=(0, 5))

target_entry = tk.Entry(target_frame)
target_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

target_button = tk.Button(target_frame, text="Browse", command=select_target)
target_button.pack(side=tk.LEFT, padx=(5, 0))

create_button = tk.Button(root, text="Create Symbolic Link", command=create_symbolic_link)
create_button.pack(fill=tk.X, padx=10, pady=(0, 5))

result_label = tk.Label(root, text="Result:")
result_label.pack(anchor=tk.W, padx=10, pady=(0, 5))

# Create a frame to hold the Text widget and scrollbar
text_frame = tk.Frame(root)
text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

# Create a Text widget for the status
status_text = tk.Text(text_frame, wrap="word", height=5)
status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0), pady=(0, 0))

# Add a scrollbar for the Text widget
scrollbar = tk.Scrollbar(text_frame, command=status_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure tags for different message types
status_text.tag_configure("error", foreground="red")

# Connect the scrollbar to the Text widget
status_text.config(yscrollcommand=scrollbar.set)

# Update the window to force it to calculate its size
root.update()

# Set minimum window size
root.minsize(root.winfo_width(), root.winfo_height())

# Start the main event loop
root.mainloop()
