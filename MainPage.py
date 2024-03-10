import customtkinter as ctk

from PageController import PageController


class MainPage(ctk.CTkFrame, PageController):

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.buttons_info = self.controller.page_display_names.copy()
        # self.buttons_info.pop('MainPage', None)

        for key, value in dict(self.buttons_info).items():
            if value == 'MainPage':
                del self.buttons_info[key]

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)


        # self.grid_rowconfigure(1, weight=2)

        # buttons_info = {
        #     # "MainPage": "MainPage",
        #     "Page1": "SubPage1",
        #     "Page2": "SubPage2",
        #     "Page3": "SubPage3",
        #     "Page4": "SubPage4",
        #     "Page5": "SubPage5",
        # }

        # button_size = 100

        col_num = 0
        row_num = 0
        for text, page_name in self.buttons_info.items():
            button = ctk.CTkButton(self, text=text, command=lambda name=page_name: controller.show_page(name, controller.header_label))
            button.configure(font=("Arial", 12))

            button.grid(row=row_num, column=col_num, sticky='nsew', padx = 50, pady = 50)

            # Configure the column to have a minsize equal to the button size, ensuring a square shape
            self.grid_columnconfigure(col_num)

            col_num += 1  # Increment counter for each button

            if col_num == 3:
                row_num += 1
                col_num = 0





        # buttons_info = {
        #     "SubPage 1": "SubPage1",
        #     "SubPage 2": "SubPage2",
        #     "SubPage 3": "SubPage3",
        #     "SubPage 4": "SubPage4",
        #     "SubPage 5": "SubPage5"
        # # }
        #
        #
        # button1 = ctk.CTkButton(self, text="Button1", font=('Arial', 16))
        # button1.grid(column=0, row=0, sticky='nsew', padx = 50, pady = 50)
        #
        # button2 = ctk.CTkButton(self, text="Button2", font=('Arial', 16))
        # button2.grid(column=1, row=0, sticky='nsew', padx = 50, pady = 50)
        #
        # button3 = ctk.CTkButton(self, text="Button3", font=('Arial', 16))
        # button3.grid(column=2, row=0, sticky='nsew', padx = 50, pady = 50)
        #
        # button4 = ctk.CTkButton(self, text="Button4", font=('Arial', 16))
        # button4.grid(column=0, row=1, sticky='nsew', padx = 50, pady = 50)
        #
        # button5 = ctk.CTkButton(self, text="Button5", font=('Arial', 16))
        # button5.grid(column=1, row=1, sticky='nsew', padx = 50, pady = 50)

