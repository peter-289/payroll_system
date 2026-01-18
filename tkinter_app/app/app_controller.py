import tkinter as tk
from jose import jwt, JWTError
from tkinter_app.app.login_frame import LoginFrame

class AppController:
    def __init__(self, tk_root: tk.Tk):
        self.root = tk_root
        self.frames = {}
        self.token = None
        self.user_claims = None

    
    def register_frame(self, frame_name: str, frame):
        self.frames[frame_name] = frame


    def show_frame(self, frame_name: str):
        if frame_name not in self.frames:
            raise ValueError(f"Frame '{frame_name}' is not registered.")
        frame = self.frames[frame_name]
        frame.tkraise()

    
    def on_login_success(self, token: str):
            self.token = token
            self.user_claims = self.decode_token(token)

            if self.user_claims.get("must_change_password"):
               self.show_frame("ChangePassword")
            else:
               self.route_by_role()
    

    def decode_token(self, token: str):
        try:
            claims = jwt.decode(token, options={"verify_signature": False})
            return claims
        except JWTError as e:
            print(f"Error decoding token: {e}")
            return None
        
    def route_by_role(self):
        role = self.user_claims.get("role")

        if role == "admin":
            self.show_frame("Admin")
        elif role == "hr":
            self.show_frame("HR")
        elif role == "employee":
            self.show_frame("Employee")
        else:
            self.logout()
            raise RuntimeError("Invalid role in token")
    
    def on_password_change_success(self, new_token: str):
        self.token = new_token
        self.user_claims = self.decode_token(new_token)
        self.route_by_role()


    def logout(self):
        self.token = None
        self.user_claims = None
        self.show_frame("Login")

    def start(self):
        self.show_frame("Login")

AppController.start()