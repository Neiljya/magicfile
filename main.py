import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Listbox, Scrollbar
from PIL import Image, ImageTk
import os
import magicfile

class FileSorterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Magic File')
        self.geometry('700x800')

        # Load and scale the image
        self.load_and_scale_logo('assets/logo.png', scale_factor=0.5)
        self.filetype_limits = {}
        self.default_limit = None
        self.directory = None
        self.create_widgets()

    def load_and_scale_logo(self, image_path, scale_factor=1.0):
        original_image = Image.open(image_path)
        # Calculate new dimensions
        width, height = original_image.size
        new_dimensions = (int(width * scale_factor), int(height * scale_factor))
        # Resize the image using the new dimensions
        scaled_image = original_image.resize(new_dimensions, Image.Resampling.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(scaled_image)

    def create_widgets(self):
        # Logo display using PhotoImage
        self.logo = tk.Label(self, image=self.logo_image)
        self.logo.grid(row=0, column=0, columnspan=2, pady=20)


        # Frame for buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, sticky='nw', padx=20)

        # Load Directory
        self.load_button = tk.Button(self.button_frame, text="Load Directory", command=self.load_directory, font=('Helvetica', 12))
        self.load_button.pack(fill=tk.X, pady=5)

        # Setting limits
        self.limit_button = tk.Button(self.button_frame, text="Set Limits", command=self.set_limits, font=('Helvetica', 12))
        self.limit_button.pack(fill=tk.X, pady=5)

        # Sort files button
        self.sort_button = tk.Button(self.button_frame, text="Sort Files", command=self.sort_files, font=('Helvetica', 12))
        self.sort_button.pack(fill=tk.X, pady=5)


        # Rename Files Button
        self.rename_button = tk.Button(self.button_frame, text="Rename Files", command=self.rename_files)
        self.rename_button.pack(fill=tk.X, pady=5)

        # Change File Type Button
        self.change_type_button = tk.Button(self.button_frame, text="Change File Type", command=self.change_file_type)
        self.change_type_button.pack(fill=tk.X, pady=5)

        # Display current directory
        self.dir_label = tk.Label(self.button_frame, text="No directory selected", font=('Helvetica', 12))
        self.dir_label.pack(fill=tk.X, pady=5)

        # Frame for file list and scrollbar
        self.file_frame = tk.Frame(self)
        self.file_frame.grid(row=1, column=1, sticky='ne', padx=20)

        # File list display
        self.file_list = Listbox(self.file_frame, width=50, height=20, font=('Helvetica', 12))
        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the file list
        self.scrollbar = Scrollbar(self.file_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.file_list.yview)
        self.file_list.config(yscrollcommand=self.scrollbar.set)

    def load_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.dir_label.config(text=f"Directory: {self.directory}")
            self.update_file_list()

    def update_file_list(self):
        if self.directory:
            self.file_list.delete(0, tk.END)
            for file in os.listdir(self.directory):
                self.file_list.insert(tk.END, file)

    def set_limits(self):
        filetype = simpledialog.askstring("Set Limit", "Enter file type (leave empty for default limit):")
        if filetype:
            # Ask for the limit of the specific file type
            limit = simpledialog.askinteger("Set Limit", f"Enter limit for {filetype} (0 for no limit):")
            if limit is not None:
                self.filetype_limits[filetype] = None if limit == 0 else limit
                messagebox.showinfo("Info", f"Limit set for {filetype}: {'Unlimited' if limit == 0 else limit}")
        else:
            # Set a default limit that applies to all unspecified file types
            default_limit = simpledialog.askinteger("Set Default Limit",
                                                    "Enter default limit for all file types (0 for no limit):")
            if default_limit is not None:
                self.default_limit = None if default_limit == 0 else default_limit
                messagebox.showinfo("Info", "Default limit set successfully: " + (
                    "Unlimited" if default_limit == 0 else str(default_limit)))
        self.update_limits_display()

    def update_limits_display(self):

        limit_text = "Current File Type Limits:\n"
        for ft, lim in self.filetype_limits.items():
            limit_text += f"{ft}: {'Unlimited' if lim is None else lim}\n"
        limit_text += f"Default Limit: {'Unlimited' if self.default_limit is None else self.default_limit}"
        messagebox.showinfo("Current Limits", limit_text)

    def sort_files(self):
        if not self.directory:
            messagebox.showerror("Error", "Load a directory first!")
            return

            # Only use explicitly set limits; ignore all other files.
        if not self.filetype_limits:
            messagebox.showinfo("Info", "No file type limits are set. No files will be sorted.")
            return

            # Call the sorting function with the determined limits
        magicfile.sort_files(self.directory, self.filetype_limits)
        messagebox.showinfo("Success", "Files have been sorted.")
        self.update_file_list()


    def rename_files(self):
        if self.directory:
            answer = messagebox.askyesno("Rename Files", "Do you want to use a custom name for renaming?")
            file_types = self.collect_file_types(self.directory)
            if answer:
                custom_name = simpledialog.askstring("Rename Files", "Enter custom file name:")
                if custom_name:
                    magicfile.rename_files(self.directory, file_types, use_custom_name=True, custom_name=custom_name)
            else:
                magicfile.rename_files(self.directory, file_types, use_custom_name=False)
            messagebox.showinfo("Success", "Files have been renamed.")
            self.update_file_list()
        else:
            messagebox.showerror("Error", "No directory selected.")

    def change_file_type(self):
        if self.directory:
            old_type = simpledialog.askstring("Change File Type", "Enter old file type (e.g., 'txt'):")
            new_type = simpledialog.askstring("Change File Type", "Enter new file type (e.g., 'md'):")
            if old_type and new_type:
                magicfile.change_file_type(self.directory, old_type, new_type)
                messagebox.showinfo("Success", "File types have been changed.")
                self.update_file_list()
        else:
            messagebox.showerror("Error", "No directory selected.")

    def collect_file_types(self, directory):
        file_types = {}
        for file in os.listdir(directory):
            full_path = os.path.join(directory, file)
            if os.path.isfile(full_path):
                ext = file.rsplit('.', 1)[1] if '.' in file else 'no_extension'
                if ext not in file_types:
                    file_types[ext] = []
                file_types[ext].append(full_path)
        return file_types

if __name__ == "__main__":
    app = FileSorterApp()
    app.mainloop()