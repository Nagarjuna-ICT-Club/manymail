import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
from email_handler import EmailHandler
from utils import insert_variable

class EmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk Email Sender")
        self.root.geometry("800x650")
        self.root.configure(bg="#f0f2f5")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#ffffff")
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

        self.generated_emails = []
        self.attachments = []
        self.email_handler = EmailHandler()

    def setup_tab1(self):
        # Set up email template tab
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Email Template')

        ttk.Label(self.tab1, text="Email Subject:").pack(pady=(10, 0), anchor='w', padx=10)
        self.subject_entry = ttk.Entry(self.tab1, width=100)
        self.subject_entry.pack(padx=10, pady=5, fill='x')

        ttk.Label(self.tab1, text="Write your email template below:").pack(pady=(10, 0), anchor='w', padx=10)
        self.template_text = tk.Text(self.tab1, wrap='word', height=20, font=("Helvetica", 12), bg="#fdfdfd")
        self.template_text.pack(padx=10, pady=5, fill='both', expand=True)

        btn_frame = ttk.Frame(self.tab1)
        btn_frame.pack(pady=10)

        self.var_entry = ttk.Entry(btn_frame, width=25)
        self.var_entry.insert(0, "name")
        self.var_entry.pack(side='left', padx=5, pady=5)

        make_var_btn = ttk.Button(btn_frame, text="Make Selected Text a Variable", command=self.insert_variable)
        make_var_btn.pack(side='left', padx=5, pady=5)

    def insert_variable(self):
        insert_variable(self.template_text, self.var_entry)

    def setup_tab2(self):
        # Set up recipients tab
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Recipients')

        ttk.Label(self.tab2, text="Enter recipient info (one per line): Name <email>").pack(pady=(10, 5), padx=10, anchor='w')

        self.recipients_text = tk.Text(self.tab2, height=10, font=("Helvetica", 12), bg="#fdfdfd", wrap='word')
        self.recipients_text.pack(padx=10, pady=5, fill='both', expand=True)

        process_btn = ttk.Button(self.tab2, text="Generate Preview", command=self.process_recipients)
        process_btn.pack(pady=10)

        ttk.Label(self.tab2, text="Preview:").pack(padx=10, anchor='w')
        self.preview_text = tk.Text(self.tab2, height=10, font=("Helvetica", 12), bg="#f9f9f9", wrap='word')
        self.preview_text.pack(padx=10, pady=5, fill='both', expand=True)

        attach_btn = ttk.Button(self.tab2, text="Attach File(s)", command=self.attach_file)
        attach_btn.pack(pady=10)

    def process_recipients(self):
        template = self.template_text.get("1.0", tk.END)
        subject_template = self.subject_entry.get()
        lines = self.recipients_text.get("1.0", tk.END).strip().split('\n')
        self.generated_emails.clear()
        self.preview_text.delete("1.0", tk.END)

        for line in lines:
            email, name = self.email_handler.parse_recipient(line)
            if email:
                personalized_content, personalized_subject = self.email_handler.generate_email_content(name, email, template, subject_template)
                self.generated_emails.append((email, personalized_subject, personalized_content))
                self.preview_text.insert(tk.END, f"To: {email}\nSubject: {personalized_subject}\n{personalized_content}\n{'-'*40}\n")
            else:
                self.preview_text.insert(tk.END, f"Invalid format: {line}\n")

    def attach_file(self):
        files = filedialog.askopenfilenames(title="Select Attachments")
        if files:
            self.attachments.extend(files)
            messagebox.showinfo("Files Attached", f"{len(files)} file(s) attached.")

    def setup_tab3(self):
        # Set up sender info tab
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Sender Info')

        frame = ttk.Frame(self.tab3)
        frame.pack(pady=30, padx=10, fill='x')

        ttk.Label(frame, text="Sender Email:").grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.sender_email_entry = ttk.Entry(frame, width=45)
        self.sender_email_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.sender_password_entry = ttk.Entry(frame, show="*", width=45)
        self.sender_password_entry.grid(row=1, column=1, padx=10, pady=10)

        send_btn = ttk.Button(self.tab3, text="Send All Emails", command=self.send_emails)
        send_btn.pack(pady=20)

    def send_emails(self):
        sender_email = self.sender_email_entry.get().strip()
        sender_pass = self.sender_password_entry.get().strip()

        if not sender_email or not sender_pass:
            messagebox.showerror("Missing Info", "Please enter your email and password.")
            return

        if not self.generated_emails:
            messagebox.showerror("No Emails", "No generated emails to send. Please generate first.")
            return

        success_count = 0
        fail_count = 0

        for recipient_email, subject, content in self.generated_emails:
            try:
                self.email_handler.send_email(sender_email, sender_pass, recipient_email, subject, content, self.attachments)
                success_count += 1
            except Exception as e:
                fail_count += 1
                print(f"Failed to send to {recipient_email}: {e}")

        messagebox.showinfo("Finished", f"Emails sent!\nSuccess: {success_count}\nFailed: {fail_count}")
