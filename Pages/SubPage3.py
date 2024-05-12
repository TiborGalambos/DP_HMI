from tkinter import ttk

import customtkinter as ctk

from Managers.CommunicationManager import CommunicationManager


class SubPage3(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.settings_container_header_label = None
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.settings_container = ctk.CTkFrame(self, fg_color="transparent")
        self.setting_container()

        self.set_container_label()

        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=1, column=0, padx=100, pady=(0,60), columnspan=3, sticky='news')

        min_button_width, min_button_height = 100, 40
        for i in range(3):
            self.settings_container.grid_columnconfigure(i, weight=1, minsize=min_button_width)
            self.settings_container.grid_rowconfigure(i + 2, weight=1,
                                                      minsize=min_button_height)
        self.selected_button = None

        # message buttons
        self.buttons = {}
        self.create_buttons()

        # reset button
        self.reset_btn = ctk.CTkButton(self.settings_container, text="Ukončiť mimoriadnu správu", command=self.reset_selection, font=("Arial", 20), fg_color="green")
        self.reset_btn.grid(row=5, column=0, columnspan=3, pady=(120,60), sticky="nsew", padx=(1400,60), ipady=30)

        self.assign_message_texts()

    def set_container_label(self):
        self.settings_container_header_label = ctk.CTkLabel(self.settings_container,
                                                            text="Mimoriadne správy pre cestujúcich",
                                                            font=("Arial", 30), anchor='center')
        self.settings_container_header_label.grid(row=0, column=0, sticky="ew", pady=(40, 50), columnspan=1)

    def create_buttons(self):
        for btn_id in range(7):
            row, col = divmod(btn_id, 3)
            text = f"Button {btn_id + 1}"

            btn = ctk.CTkButton(self.settings_container, text=text,
                                command=lambda b=btn_id: self.button_clicked(b), fg_color="#144870")

            btn.grid(row=row + 2, column=col, pady=20, padx=30, sticky="nsew", ipady=60, ipadx=40)
            self.buttons[btn_id] = (btn, text)

    def assign_message_texts(self):
        self.configure_button_text(0, "Nenastupovať")
        self.configure_button_text(1, "Mimo prevádzky")
        self.configure_button_text(2, "Testovacia jazda")
        self.configure_button_text(3, "Porucha vlaku")
        self.configure_button_text(4, "Služobná jazda")
        self.configure_button_text(5, "Vozidlo preťažené")
        self.configure_button_text(6, "Núdzová brzda aktivovaná")

    # configuration set of the setting container
    def setting_container(self):
        self.settings_container.grid(row=0, column=0, sticky="news", padx=20, pady=20)
        for i in range(3):
            self.settings_container.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.settings_container.grid_rowconfigure(i, weight=0)

    # handle button click
    def button_clicked(self, btn_id):
        if self.selected_button is not None:
            self.selected_button[0].configure(fg_color="#144870") # default color

        self.selected_button = self.buttons[btn_id]
        self.selected_button[0].configure(fg_color="#0c2b43")  # dark color

        button_text = self.selected_button[1]
        com_man = CommunicationManager.get_instance()
        com_man.send_basic_message(button_text)

    def reset_selection(self):
        if self.selected_button is not None:
            button, _ = self.selected_button
            button.configure(fg_color="#144870")
            self.selected_button = None
            print("reset selected")
            com_man = CommunicationManager.get_instance()
            com_man.reset_message()

    # get button by id
    def configure_button_text(self, btn_id, text):
        if btn_id in self.buttons:
            button, _ = self.buttons[btn_id]
            button.configure(text=text, font=("Arial", 30))
            self.buttons[btn_id] = (button, text)
        else:
            print(f"button not found - id: {btn_id}")


