import tkinter as tk
import requests

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self._build_ui()


    def _build_ui(self):
        tk.Label(self, text="Username").pack()
        tk.Entry(self, textvariable=self.username_var).pack()

        tk.Label(self, text="Password").pack()
        tk.Entry(self, textvariable=self.password_var, show="*").pack()

        tk.Button(self, text="Login", command=self.login).pack()

        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack()
    

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if not username or not password:
            self.error_label.config(text="Username and password required")
            return

        try:
            response = requests.post(
                "http://localhost:8000/auth/login",
                data={
                    "username": username,
                    "password": password
                }
            )
            if response.status_code != 200:
               self.error_label.config(text="Invalid credentials")
            

            data = response.json()
            token = data.get("access_token")

            if not token:
               self.error_label.config(text="Invalid server response")
               return

            self.controller.on_login_success(token)
        except requests.RequestException:
            self.error_label.config(text="Server unavailable")
            return
