import tkinter as tk
from tkinter import messagebox
import requests


BASE_URL = "http://127.0.0.1:8000/auth/login"
def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Validation error!", "Please enter username and password correctly!")
        return 
    try:
        response = requests.post(f"{BASE_URL}", data={"username":username, "password":password})
        if response.status_code == 200:
            messagebox.showinfo("Success",response.json().get("access_token"))
        else: 
            messagebox.showerror("Failed", response.json().get("detail"))
            message = response.json().get("detail")
            print(f"Error: {message}")
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Error", "Can not connect to server!. Check if fastAPI is running!")

root = tk.Tk()
root.title("Login Window")
root.geometry("500x400")
tk.Label(root, text="Username").pack(pady=(20, 5))
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Password.").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()
