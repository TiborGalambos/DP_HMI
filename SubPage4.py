import time
from tkinter import ttk

import customtkinter as ctk

from CommunicationManager import CommunicationManager
from DatabaseManager import DatabaseManager
import threading

class SubPage4(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller


        self.grid_columnconfigure(0, weight=1)
        self.diagnostics_container = ctk.CTkFrame(self)
        self.diagnostics_container.grid(row=0, column=0, sticky="news", padx=20, pady=20)
        self.diagnostics_container.grid_columnconfigure(0, weight=1)
        self.diagnostics_container.grid_columnconfigure(1, weight=1)
        self.diagnostics_container.grid_columnconfigure(2, weight=1)

        self.diagnostics_container.grid_rowconfigure(0, weight=0)
        self.diagnostics_container.grid_rowconfigure(1, weight=0)
        self.diagnostics_container.grid_rowconfigure(2, weight=0)
        self.diagnostics_container.grid_rowconfigure(3, weight=0)
        self.diagnostics_container.grid_rowconfigure(4, weight=0)
        self.diagnostics_container.grid_rowconfigure(5, weight=0)
        self.diagnostics_container.grid_rowconfigure(6, weight=0)
        self.diagnostics_container.grid_rowconfigure(7, weight=0)

        self.server_test_button = ctk.CTkButton(self.diagnostics_container, text="Spustiť",
                            command=self.server_test, fg_color="#144870")

        self.panel1_test_button = ctk.CTkButton(self.diagnostics_container, text="Spustiť",
                                           command=self.panel1_test, fg_color="#144870")

        self.panel2_test_button = ctk.CTkButton(self.diagnostics_container, text="Spustiť",
                                           command=self.panel2_test, fg_color="#144870")


        # self.diagnostics_container.grid_rowconfigure(8, weight=0)


        self.server_diagnostic_header_label = ctk.CTkLabel(self.diagnostics_container,
                                                           text="Diagnostika ovládača",
                                                           font=("Arial", 30, "bold"), anchor='center')
        self.server_diagnostic_header_label.grid(row=0, column=0, sticky="ew", pady=(40, 50), columnspan=1)

        self.server_diagnostic_header_label = ctk.CTkLabel(self.diagnostics_container,
                                                           text="Test pripojenia ovládača a prístupu na internet",
                                                           font=("Arial", 18), anchor='w')
        self.server_diagnostic_header_label.grid(row=1, column=0, sticky="ew", pady=(40, 50), padx=(30, 0), columnspan=1)

        self.server_test_button.grid(row=1, column=1, sticky="ew")

        self.separator = ttk.Separator(self.diagnostics_container)
        self.separator.grid(row=2, column=0, padx=100, pady=(0, 60), columnspan=2, sticky='news')






        self.server_diagnostic_header_label = ctk.CTkLabel(self.diagnostics_container,
                                                           text="Diagnostika panela 1",
                                                           font=("Arial", 30), anchor='center')
        self.server_diagnostic_header_label.grid(row=3, column=0, sticky="ew", pady=(40, 50), columnspan=1)

        self.server_diagnostic_header_label = ctk.CTkLabel(self.diagnostics_container,
                                                           text="Test pripojenia panela 1 odoslaním správy.",
                                                           font=("Arial", 18), anchor='w')
        self.server_diagnostic_header_label.grid(row=4, column=0, sticky="ew", pady=(40, 50), padx=(30, 0),
                                                 columnspan=1)

        self.panel1_test_button.grid(row=4, column=1, sticky="ew")

        self.separator = ttk.Separator(self.diagnostics_container)
        self.separator.grid(row=5, column=0, padx=100, pady=(0, 60), columnspan=2, sticky='news')




        self.server_diagnostic_header_label = ctk.CTkLabel(self.diagnostics_container,
                                                           text="Diagnostika panela 2",
                                                           font=("Arial", 30), anchor='center')
        self.server_diagnostic_header_label.grid(row=6, column=0, sticky="ew", pady=(40, 50), columnspan=1)

        self.server_diagnostic_header_label = ctk.CTkLabel(self.diagnostics_container,
                                                           text="Test pripojenia panela 2 odoslaním správy.",
                                                           font=("Arial", 18), anchor='w')
        self.server_diagnostic_header_label.grid(row=7, column=0, sticky="ew", pady=(40, 50), padx=(30, 0),
                                                 columnspan=1)

        self.panel2_test_button.grid(row=7, column=1, sticky="ew")



        self.result_panel_container = ctk.CTkFrame(self.diagnostics_container, width=300)
        self.result_panel_container.grid_propagate(False)
        self.result_panel_container.grid(row=0, column=2, sticky="news", padx=20, pady=20, rowspan=8)
        self.result_panel_container.grid_rowconfigure(0, weight=0)
        self.result_panel_container.grid_rowconfigure(1, weight=0)
        self.result_panel_container.grid_rowconfigure(2, weight=0)
        self.result_panel_container.grid_rowconfigure(3, weight=0)
        self.result_panel_container.grid_rowconfigure(4, weight=0)
        self.result_panel_container.grid_rowconfigure(5, weight=0)
        self.result_panel_container.grid_rowconfigure(6, weight=0)
        self.result_panel_container.grid_rowconfigure(7, weight=0)

        self.result_panel_container.grid_columnconfigure(0, weight=1)
        self.result_panel_container.grid_columnconfigure(1, weight=1)

        self.result_header_label = ctk.CTkLabel(self.result_panel_container,
                                                           text="Výsledky",
                                                           font=("Arial", 30), anchor='center')
        self.result_header_label.grid(row=0, column=0, sticky="ew", pady=(30, 50), columnspan=2)



        self.result_header_label = ctk.CTkLabel(self.result_panel_container,
                                                text="ovládač",
                                                font=("Arial", 20), anchor='center')
        self.result_header_label.grid(row=1, column=0, sticky="ew", pady=(30, 50), padx=(30, 0), columnspan=1)

        self.controller_result_label = ctk.CTkLabel(self.result_panel_container,
                                                text="N/A",
                                                font=("Arial", 20), anchor='center')
        self.controller_result_label.grid(row=1, column=1, sticky="ew", pady=(30, 50), columnspan=1)

        ####

        self.result_header_label = ctk.CTkLabel(self.result_panel_container,
                                                text="internet",
                                                font=("Arial", 20), anchor='center')
        self.result_header_label.grid(row=2, column=0, sticky="ew", pady=(30, 50), padx=(30, 0), columnspan=1)

        self.internet_result_label = ctk.CTkLabel(self.result_panel_container,
                                                    text="N/A",
                                                    font=("Arial", 20), anchor='center')
        self.internet_result_label.grid(row=2, column=1, sticky="ew", pady=(30, 50), columnspan=1)


        ####

        self.result_header_label = ctk.CTkLabel(self.result_panel_container,
                                                text="panel 1",
                                                font=("Arial", 20), anchor='center')
        self.result_header_label.grid(row=3, column=0, sticky="ew", pady=(30, 50), padx=(30, 0), columnspan=1)

        self.panel1_result_label = ctk.CTkLabel(self.result_panel_container,
                                                  text="N/A",
                                                  font=("Arial", 20), anchor='center')
        self.panel1_result_label.grid(row=3, column=1, sticky="ew", pady=(30, 50), columnspan=1)

        ####

        self.result_header_label = ctk.CTkLabel(self.result_panel_container,
                                                text="panel 2",
                                                font=("Arial", 20), anchor='center')
        self.result_header_label.grid(row=4, column=0, sticky="ew", pady=(30, 50), padx=(30, 0), columnspan=1)

        self.panel2_result_label = ctk.CTkLabel(self.result_panel_container,
                                                text="N/A",
                                                font=("Arial", 20), anchor='center')
        self.panel2_result_label.grid(row=4, column=1, sticky="ew", pady=(30, 50), columnspan=1)

        ####

        self.result_header_label = ctk.CTkLabel(self.result_panel_container,
                                                text="Posledná kontrola:",
                                                font=("Arial", 20), anchor='w')
        self.result_header_label.grid(row=5, column=0, sticky="ew", pady=(30, 50), padx=(30, 0), columnspan=2)

    def server_test(self):
        print("Server test pressed")
        self.controller_result_label.configure(text="...")

        def run_test():
            com_manager = CommunicationManager.get_instance()
            if com_manager.controller_connectivity_test():
                print("OK")
                self.controller_result_label.configure(text="OK")
            else:
                print("NOT OK")
                self.controller_result_label.configure(text="NOT OK")

            self.update_last_check_time()
            return

        test_thread = threading.Thread(target=run_test)
        test_thread.start()
        self.internet_test()

    def internet_test(self):

        print("Server test pressed")
        self.internet_result_label.configure(text="...")

        def run_test():
            com_manager = CommunicationManager.get_instance()
            if com_manager.controller_internet_connectivity_test():
                print("OK")
                self.internet_result_label.configure(text="OK")
            else:
                print("NOT OK")
                self.internet_result_label.configure(text="NOT OK")

            self.update_last_check_time()
            return

        test_thread = threading.Thread(target=run_test)
        test_thread.start()

    def panel1_test(self):
        print("Panel1 test pressed")

        self.panel1_result_label.configure(text="...")

        def run_test():
            com_manager = CommunicationManager.get_instance()
            if com_manager.display_panel_1_test():
                print("OK")
                self.panel1_result_label.configure(text="OK")
            else:
                print("NOT OK")
                self.panel1_result_label.configure(text="NOT OK")

            self.update_last_check_time()
            return

        test_thread = threading.Thread(target=run_test)
        test_thread.start()

    def panel2_test(self):
        print("Panel2 test pressed")
        self.panel2_result_label.configure(text="...")
        def run_test():
            com_manager = CommunicationManager.get_instance()
            if com_manager.display_panel_2_test():
                print("OK")
                self.panel2_result_label.configure(text="OK")
            else:
                print("NOT OK")
                self.panel2_result_label.configure(text="NOT OK")

            self.update_last_check_time()
            return

        test_thread = threading.Thread(target=run_test)
        test_thread.start()


    def update_last_check_time(self):
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%d.%m.%Y')
        self.result_header_label.configure(text=f"Posledná kontrola: {str(current_date)} {str(current_time)}")

