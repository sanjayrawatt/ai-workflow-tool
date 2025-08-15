import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os

# Import the functions from our main script
from main import run_workflow, load_config

class WorkflowApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Basic Window Setup ---
        self.title("AI Workflow Automation Tool")
        self.geometry("600x400") # Set window size

        # Load configuration
        self.config = load_config()
        if not self.config:
            messagebox.showerror("Error", "config.yaml not found or is invalid. Please fix it before running the GUI.")
            self.destroy()
            return

        # --- GUI Variables ---
        self.input_file_path = tk.StringVar(value=self.config.get('default_input_path', ''))
        self.output_file_path = tk.StringVar(value=self.config.get('default_output_path', ''))

        # --- Create Widgets ---
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Input File Selection
        ttk.Label(main_frame, text="Input Excel File:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        input_entry = ttk.Entry(main_frame, textvariable=self.input_file_path, width=60)
        input_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        ttk.Button(main_frame, text="Browse...", command=self.select_input_file).grid(row=1, column=1, sticky="ew")

        # Output File Selection
        ttk.Label(main_frame, text="Output Excel File:", font=("Helvetica", 12, "bold")).grid(row=2, column=0, sticky="w", pady=(20, 5))
        output_entry = ttk.Entry(main_frame, textvariable=self.output_file_path, width=60)
        output_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10))
        ttk.Button(main_frame, text="Browse...", command=self.select_output_file).grid(row=3, column=1, sticky="ew")

        # Run Button
        self.run_button = ttk.Button(main_frame, text="Run Workflow", command=self.start_workflow_thread, style="Accent.TButton")
        self.run_button.grid(row=4, column=0, columnspan=2, pady=(30, 10), ipady=5, sticky="ew")
        
        # Style for the big button
        style = ttk.Style(self)
        style.configure("Accent.TButton", font=("Helvetica", 12, "bold"))

        # Status Label
        self.status_label = ttk.Label(main_frame, text="Ready to start.", font=("Helvetica", 10, "italic"))
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky="w")

    def select_input_file(self):
        """Opens a dialog to select the input .xlsx file."""
        file_path = filedialog.askopenfilename(
            title="Select Input Excel File",
            filetypes=(("Excel Files", "*.xlsx"), ("All files", "*.*"))
        )
        if file_path:
            self.input_file_path.set(file_path)

    def select_output_file(self):
        """Opens a dialog to set the output .xlsx file path."""
        file_path = filedialog.asksaveasfilename(
            title="Select Output File Location",
            filetypes=(("Excel Files", "*.xlsx"), ("All files", "*.*")),
            defaultextension=".xlsx",
            initialfile="processed_data.xlsx"
        )
        if file_path:
            self.output_file_path.set(file_path)

    def start_workflow_thread(self):
        """
        Runs the workflow in a separate thread to keep the GUI responsive.
        """
        self.run_button.config(state="disabled") # Disable button during run
        self.status_label.config(text="Processing... please wait.")
        
        # Create and start the thread
        thread = threading.Thread(target=self.run_the_workflow)
        thread.start()

    def run_the_workflow(self):
        """The actual function that calls the main processing logic."""
        input_p = self.input_file_path.get()
        output_p = self.output_file_path.get()

        if not input_p or not output_p:
            messagebox.showerror("Error", "Please specify both input and output file paths.")
            self.run_button.config(state="normal")
            return

        run_workflow(input_p, output_p, self.config)
        
        # When done, update the GUI
        self.status_label.config(text=f"Workflow complete! Output saved to:\n{os.path.basename(output_p)}")
        self.run_button.config(state="normal")
        messagebox.showinfo("Success", "The workflow has completed successfully!")


if __name__ == "__main__":
    app = WorkflowApp()
    app.mainloop()
