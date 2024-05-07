from tkinter import ttk
import tkinter as tk
import customtkinter as ctk


class SubPage5(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.settings_container = ctk.CTkFrame(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.settings_container.grid(row=0, column=1, sticky="news", padx=20, pady=20)
        self.settings_container.grid_columnconfigure(0, weight=1)
        self.settings_container.grid_columnconfigure(1, weight=1)

        self.settings_container.grid_rowconfigure(0, weight=0)
        self.settings_container.grid_rowconfigure(1, weight=0)
        self.settings_container.grid_rowconfigure(2, weight=0)
        self.settings_container.grid_rowconfigure(3, weight=0)
        self.settings_container.grid_rowconfigure(4, weight=0)

        self.settings_container_header_label = ctk.CTkLabel(self.settings_container, text="Preferencie používateľa",
                                                            font=("Arial", 30), anchor='w')
        self.settings_container_header_label.grid(row=0, column=0, sticky="ew", pady=(20, 50), padx=(100, 0), columnspan=2)

        self.display_panel_settings = ctk.CTkLabel(self.settings_container, text="Vzhľad aplikácie", font=("Arial", 20),
                                                   anchor='w')
        self.display_panel_settings.grid(row=1, column=0, pady=(20, 0), padx=20)

        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=2, column=0, padx=100, pady=0, columnspan=2, sticky='news')

        self.theme_switch_setting = ctk.IntVar()  # This variable will hold the state of the checkbox, 0 for unchecked, 1 for checked
        self.theme_switch_setting.set(1)

        self.theme_switch = ctk.CTkSwitch(self.settings_container, text="Tmavý vzhľad",
                                     variable=self.theme_switch_setting,
                                     onvalue=1, offvalue=0, command=self.theme_switch, font=("Arial", 30))
        self.theme_switch.grid(row=3, column=0, pady=20, padx=20, columnspan=1)

        self.display_panel_settings = ctk.CTkLabel(self.settings_container, text="Výber portu pre komunikáciu s panelom typu 1", font=("Arial", 20),
                                                   anchor='w')
        self.display_panel_settings.grid(row=4, column=0, pady=(20, 0), padx=20)

        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=5, column=0, padx=100, pady=0, columnspan=2, sticky='news')

        # Create a CTkCheckBox

        serial_output_spinbox = SerialOutputSpinbox(self.settings_container)
        serial_output_spinbox.grid(pady=20, padx=20)

        brightness_spinbox = BrightnessSpinbox(self.settings_container)
        brightness_spinbox.grid(pady=20, padx=20)

        speed_spinbox = SpeedSpinbox(self.settings_container)
        speed_spinbox.grid(pady=20, padx=20)

    def theme_switch(self):
        pass
    def switch1_callback(self):
        pass

    def switch2_callback(self):
        pass
    def switch3_callback(self):
        pass
    def switch4_callback(self):
        pass
    def save_settings(self):
        pass


class SerialOutputSpinbox(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.value = tk.IntVar(value=1)

        self.label = ctk.CTkLabel(self, text="Číslo portu", font=("Arial", 22))
        self.label.pack(side=tk.LEFT, padx=(20, 50))

        self.dec_button = ctk.CTkButton(self, text='-', font=("Arial", 30), command=self.decrement)
        self.dec_button.pack(side=tk.LEFT, padx=5, ipady=20)


        self.entry = ctk.CTkEntry(self, textvariable=self.value, width=30, state="readonly", font=("Arial", 40))
        self.entry.pack(side=tk.LEFT, padx=5)

        self.inc_button = ctk.CTkButton(self, text='+', font=("Arial", 30), command=self.increment)
        self.inc_button.pack(side=tk.LEFT, padx=5, ipady=20)



    def increment(self):
        current_value = self.get_value()
        if current_value < 3:
            self.value.set(current_value + 1)

    def decrement(self):
        current_value = self.get_value()
        if current_value > 1:
            self.value.set(current_value - 1)

    def get_value(self):
        return self.value.get()



class BrightnessSpinbox(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.value = tk.IntVar(value=1)

        self.label = ctk.CTkLabel(self, text="Jas panela 1", font=("Arial", 22))
        self.label.pack(side=tk.LEFT, padx=(20, 50))

        self.dec_button = ctk.CTkButton(self, text='-', font=("Arial", 30), command=self.decrement)
        self.dec_button.pack(side=tk.LEFT, padx=5, ipady=20)


        self.entry = ctk.CTkEntry(self, textvariable=self.value, width=30, state="readonly", font=("Arial", 40))
        self.entry.pack(side=tk.LEFT, padx=5)

        self.inc_button = ctk.CTkButton(self, text='+', font=("Arial", 30), command=self.increment)
        self.inc_button.pack(side=tk.LEFT, padx=5, ipady=20)


    def increment(self):
        current_value = self.get_value()
        if current_value < 5:
            self.value.set(current_value + 1)

    def decrement(self):
        current_value = self.get_value()
        if current_value > 1:
            self.value.set(current_value - 1)

    def get_value(self):
        return self.value.get()


class SpeedSpinbox(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.value = tk.IntVar(value=1)

        self.label = ctk.CTkLabel(self, text="Rýchlosť", font=("Arial", 22))
        self.label.pack(side=tk.LEFT, padx=(20, 50))

        self.dec_button = ctk.CTkButton(self, text='-', font=("Arial", 30), command=self.decrement)
        self.dec_button.pack(side=tk.LEFT, padx=5, ipady=20)


        self.entry = ctk.CTkEntry(self, textvariable=self.value, width=30, state="readonly", font=("Arial", 40))
        self.entry.pack(side=tk.LEFT, padx=5)

        self.inc_button = ctk.CTkButton(self, text='+', font=("Arial", 30), command=self.increment)
        self.inc_button.pack(side=tk.LEFT, padx=5, ipady=20)


    def increment(self):
        current_value = self.get_value()
        if current_value < 5:
            self.value.set(current_value + 1)

    def decrement(self):
        current_value = self.get_value()
        if current_value > 1:
            self.value.set(current_value - 1)

    def get_value(self):
        return self.value.get()