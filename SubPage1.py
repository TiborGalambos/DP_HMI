import customtkinter as ctk


class SubPage1(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        label = ctk.CTkLabel(self, text="This is subpage 1")
        label.pack(pady=10, padx=10)
