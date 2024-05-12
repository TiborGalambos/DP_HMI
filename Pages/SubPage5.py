from tkinter import ttk
import tkinter as tk

import customtkinter
import customtkinter as ctk

from Managers.DatabaseManager import DatabaseManager


class SubPage5(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.settings_container = ctk.CTkFrame(self)
        self.setting_container_init()

        self.setting_controllers_init()
        self.db_manager = DatabaseManager()

        self.set_from_db()

    # Initialize the setting controllers, buttons, switches and the labels.

    def setting_controllers_init(self):
        self.display_panel_settings = ctk.CTkLabel(self.settings_container, text="Vzhľad aplikácie", font=("Arial", 25))
        self.display_panel_settings.grid(row=0, column=0, pady=(20, 0), padx=70, sticky="w")
        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=1, column=0, padx=100, pady=0, columnspan=2, sticky='news')
        self.theme_switch_setting = ctk.IntVar()
        self.theme_switch_setting.set(1)
        self.theme_switch = ctk.CTkSwitch(self.settings_container, text="Tmavý vzhľad",
                                          variable=self.theme_switch_setting,
                                          onvalue=1, offvalue=0, font=("Arial", 30))
        self.theme_switch.grid(row=2, column=0, pady=20, padx=20, columnspan=1)
        self.display_panel_settings = ctk.CTkLabel(self.settings_container,
                                                   text="Výber portu pre komunikáciu s panelom typu 2",
                                                   font=("Arial", 25))
        self.display_panel_settings.grid(row=3, column=0, pady=(20, 0), padx=70, sticky="w")
        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=4, column=0, padx=100, pady=0, columnspan=2, sticky='news')
        self.serial_output_spinbox = SerialOutputSpinbox(self.settings_container)
        self.serial_output_spinbox.grid(row=5, pady=20, padx=20)
        self.display_panel_settings = ctk.CTkLabel(self.settings_container,
                                                   text="Nastavenie jasu na paneli typu 1",
                                                   font=("Arial", 25))
        self.display_panel_settings.grid(row=6, column=0, pady=(20, 0), padx=70, sticky="w")
        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=7, column=0, padx=100, pady=0, columnspan=2, sticky='news')
        self.brightness_switch_setting = ctk.IntVar()
        self.brightness_switch_setting.set(1)
        self.brightness_spinbox = BrightnessSpinbox(self.settings_container, self.brightness_switch_setting)
        self.brightness_spinbox.grid(row=8, pady=20, padx=20)
        self.brightness_switch = ctk.CTkSwitch(self.settings_container, text="Automatický",
                                               variable=self.brightness_switch_setting,
                                               onvalue=1, offvalue=0, command=self.brightness_switch,
                                               font=("Arial", 30))
        self.brightness_switch.grid(row=9, column=0, pady=20, padx=20, columnspan=1)
        self.display_panel_settings = ctk.CTkLabel(self.settings_container,
                                                   text="Nastavenie rýchlosti prechodu obsahu na paneloch",
                                                   font=("Arial", 25))
        self.display_panel_settings.grid(row=10, column=0, pady=(20, 0), padx=70, sticky="w")
        self.separator = ttk.Separator(self.settings_container)
        self.separator.grid(row=11, column=0, padx=100, pady=0, columnspan=2, sticky='news')
        self.speed_spinbox = SpeedSpinbox(self.settings_container)
        self.speed_spinbox.grid(row=12, pady=20, padx=20)
        self.save_settings_button = ctk.CTkButton(self.settings_container, text="Uložiť nastavenia", fg_color='green',
                                                  font=("Arial", 30), hover_color='darkgreen',
                                                  command=self.save_settings)
        self.save_settings_button.grid(row=13, column=0, sticky='ns', pady=30, padx=100, ipadx=20, ipady=30,
                                       columnspan=2)

    # init the container of the subpage
    def setting_container_init(self):
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        self.settings_container.grid(row=0, column=1, sticky="news", padx=20, pady=20)
        self.settings_container.grid_columnconfigure(0, weight=1)
        self.settings_container.grid_columnconfigure(1, weight=1)
        for i in range(14):
            self.settings_container.grid_rowconfigure(i, weight=0)

    # set values from database at init
    def set_from_db(self):
        settings = self.db_manager.get_settings()[0]

        if settings[0] == "dark":
            self.theme_switch_setting.set(1)
            customtkinter.set_appearance_mode("dark")
        else:
            self.theme_switch_setting.set(0)
            customtkinter.set_appearance_mode("light")

        self.serial_output_spinbox.value.set(settings[1])
        self.brightness_spinbox.value.set(settings[2])

        if settings[2] == 0:
            self.brightness_switch_setting.set(1)
        else:
            self.brightness_switch_setting.set(0)

        self.speed_spinbox.value.set(settings[3])

    def brightness_switch(self):
        if self.brightness_switch_setting.get() == 1:
            self.brightness_spinbox.value.set(0)
        else:
            self.brightness_spinbox.value.set(1)

    # save sttings to database
    def save_settings(self):
        theme=self.theme_switch_setting.get()
        if theme:
            theme="dark"
            customtkinter.set_appearance_mode("dark")
        else:
            theme="light"
            customtkinter.set_appearance_mode("light")

        port = str(self.serial_output_spinbox.get_value())
        brightness = str(self.brightness_spinbox.get_value())
        speed = str(self.speed_spinbox.get_value())

        self.db_manager.update_setting(theme, port, brightness, speed)

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
    def __init__(self, parent, brightness_switch_setting, **kwargs):
        super().__init__(parent, **kwargs)
        self.brightness_switch_setting = brightness_switch_setting
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
        if self.get_value() > 0:
            self.brightness_switch_setting.set(0)

    def decrement(self):
        current_value = self.get_value()
        if current_value > 0:
            self.value.set(current_value - 1)
        if self.get_value() == 0:
            self.brightness_switch_setting.set(1)

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
