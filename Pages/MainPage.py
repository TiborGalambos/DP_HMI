import customtkinter as ctk


# Main page of the GUI, contains several buttons that together act as the main menu.
class MainPage(ctk.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.buttons_info = self.controller.page_display_names.copy()

        for key, value in dict(self.buttons_info).items():
            if value == 'MainPage':
                del self.buttons_info[key]

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_columnconfigure(2, weight=1)

        col_num = 0
        row_num = 0
        icon_num = 1

        self.controller.load_icons()
        icons = self.controller.get_icons()

        for text, page_name in self.buttons_info.items():
            button = ctk.CTkButton(self, text=text, image = icons[icon_num], command=lambda name=page_name: controller.show_page(name, self.controller.header_label), corner_radius=100000)
            button.configure(font=("Arial", 25))

            button.grid(row=row_num, column=col_num, sticky='nsew', padx = 50, pady = 50)

            self.grid_columnconfigure(col_num)

            icon_num += 1
            col_num += 1

            if col_num == 3:
                row_num += 1
                col_num = 0




