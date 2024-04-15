from tkinter import ttk

import customtkinter as ctk

from CommunicationManager import CommunicationManager


class SubPage3(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.settings_container = ctk.CTkFrame(self)
        self.settings_container.grid(row=0, column=0, sticky="news", padx=20, pady=20)
        self.settings_container.grid_columnconfigure(0, weight=1)
        self.settings_container.grid_columnconfigure(1, weight=1)
        self.settings_container.grid_columnconfigure(2, weight=1)

        self.settings_container.grid_rowconfigure(0, weight=0)
        self.settings_container.grid_rowconfigure(1, weight=0)
        self.settings_container.grid_rowconfigure(2, weight=0)
        self.settings_container.grid_rowconfigure(3, weight=0)
        self.settings_container.grid_rowconfigure(4, weight=0)

        self.settings_container_header_label = ctk.CTkLabel(self.settings_container, text="Mimoriadne správy pre cestujúcich",
                                                            font=("Arial", 30), anchor='center')
        self.settings_container_header_label.grid(row=0, column=0, sticky="ew", pady=(40, 50), columnspan=1)

        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=1, column=0, padx=100, pady=(0,60), columnspan=3, sticky='news')

        # Configure grid columns for a 3x3 layout
        min_button_width, min_button_height = 100, 40  # Set your desired minimum button dimensions here
        for i in range(3):  # Assuming a 3x3 grid
            self.settings_container.grid_columnconfigure(i, weight=1, minsize=min_button_width)
            self.settings_container.grid_rowconfigure(i + 2, weight=1,
                                                      minsize=min_button_height)  # Rows start from 2 in your setup

        # Initialize variable to keep track of the selected button
        self.selected_button = None

        # Dictionary to store button references
        self.buttons = {}

        # Add buttons in a 3x3 grid, but only create 7 buttons
        for btn_id in range(7):
            row, col = divmod(btn_id, 3)
            text = f"Button {btn_id + 1}"
            btn = ctk.CTkButton(self.settings_container, text=text,
                                command=lambda b=btn_id: self.button_clicked(b), fg_color="#144870")
            btn.grid(row=row + 2, column=col, pady=20, padx=30, sticky="nsew", ipady=60, ipadx=40)
            self.buttons[btn_id] = (btn, text)  # Store both the button and its text

        # Add a reset button below the 3x3 grid
        self.reset_btn = ctk.CTkButton(self.settings_container, text="Ukončiť mimoriadnu správu", command=self.reset_selection, font=("Arial", 20), fg_color="green")
        self.reset_btn.grid(row=5, column=0, columnspan=3, pady=(150,60), sticky="nsew", padx=(1400,60), ipady=30)

        self.configure_button_text(0, "Nenastupovať")
        self.configure_button_text(1, "Mimo prevádzky")
        self.configure_button_text(2, "Testovacia jazda")
        self.configure_button_text(3, "Porucha vlaku")
        self.configure_button_text(4, "Služobná jazda")
        self.configure_button_text(5, "Vozidlo preťažené")
        self.configure_button_text(6, "Núdzová brzda aktivovaná")

    def button_clicked(self, btn_id):
        if self.selected_button is not None:
            self.selected_button[0].configure(fg_color="#144870")  # Reset to default color using index 0 for the button

        # Update the selected button and change its appearance
        self.selected_button = self.buttons[btn_id]
        self.selected_button[0].configure(fg_color="#0c2b43")  # Set to a darker color to indicate selection

        # Access button text stored as part of the tuple
        button_text = self.selected_button[1]  # Using index 1 for the text
        # print(f"Button {btn_id + 1} with text '{button_text}' was pressed")
        com_man = CommunicationManager.get_instance()
        com_man.send_basic_message(button_text)


    def reset_selection(self):
        if self.selected_button is not None:
            button, _ = self.selected_button  # Unpack the tuple to get the button object
            button.configure(fg_color="#144870")  # Reset to default color using the button object
            self.selected_button = None
            print("Selection reset")
            com_man = CommunicationManager.get_instance()
            com_man.send_basic_message(' ')


    def configure_button_text(self, btn_id, text):
        """Configure the text of a button given its ID."""
        if btn_id in self.buttons:
            button, _ = self.buttons[btn_id]  # Unpack the tuple to get the button object
            button.configure(text=text, font=("Arial", 30))  # Configure the button
            self.buttons[btn_id] = (button, text)  # Update the tuple with new text
        else:
            print(f"Button with ID {btn_id} not found")


