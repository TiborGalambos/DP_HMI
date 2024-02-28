import customtkinter as ctk


class MainPage(ctk.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_columnconfigure(2, weight=1)


        # self.grid_rowconfigure(1, weight=2)


        button1 = ctk.CTkButton(self, text="Button1", font=('Arial', 16))
        button1.grid(column=0, row=0, sticky='nsew', padx = 50, pady = 50)

        button2 = ctk.CTkButton(self, text="Button2", font=('Arial', 16))
        button2.grid(column=1, row=0, sticky='nsew', padx = 50, pady = 50)

        button3 = ctk.CTkButton(self, text="Button3", font=('Arial', 16))
        button3.grid(column=2, row=0, sticky='nsew', padx = 50, pady = 50)

        button4 = ctk.CTkButton(self, text="Button4", font=('Arial', 16))
        button4.grid(column=0, row=1, sticky='nsew', padx = 50, pady = 50)

        button5 = ctk.CTkButton(self, text="Button5", font=('Arial', 16))
        button5.grid(column=1, row=1, sticky='nsew', padx = 50, pady = 50)





        # header_label.pack(side='top', pady=(10, 20),)
        #
        # # Content section
        # content_frame = ctk.CTkFrame(self)
        # content_frame.pack(expand=True, fill='both', padx=20, pady=20)
        # content_label = ctk.CTkLabel(content_frame, text="Main Content Area", font=('Arial', 12))
        # content_label.pack(side='top', pady=10)
        #
        # # Example of additional content
        # for i in range(5):
        #     item_label = ctk.CTkLabel(content_frame, text=f"Item {i+1}", font=('Arial', 10))
        #     item_label.pack(pady=2)
        #
        # # Footer section
        # footer_frame = ctk.CTkFrame(self)
        # footer_frame.pack(fill='x', pady=10)
        # footer_label = ctk.CTkLabel(footer_frame, text="Footer Information", font=('Arial', 10))
        # footer_label.pack(side='top', pady=(10, 20))
