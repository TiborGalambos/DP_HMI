import customtkinter as ctk

from SubPage5 import SubPage5
from SubPage4 import SubPage4
from SubPage3 import SubPage3
from SubPage2 import SubPage2
from SubPage1 import SubPage1
from MainPage import MainPage



class AppMainLayout(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.page_display_names = {
            "MainPage": "Výber aplikácie",
            "SubPage1": "Sub Page 1",
            "SubPage2": "Sub Page 2",
            "SubPage3": "Sub Page 3",
            "SubPage4": "Sub Page 4",
            "SubPage5": "Sub Page 5",
        }

        self.title('HMI')
        self.geometry('1000x650')
        self.grid_rowconfigure(0, weight=0)  # Header row should not expand
        self.grid_rowconfigure(1, weight=1)  # Content row should expand
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Container for all pages
        self.pages_container = ctk.CTkFrame(self, width=300, height=300)
        self.pages_container.grid(row=0, column=0, sticky='nsew')

        # Pages
        self.pages = {}
        for F in (MainPage, SubPage1, SubPage2, SubPage3, SubPage4, SubPage5):
            page_name = F.__name__
            page = F(master=self.pages_container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")


        # Header frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky='ew')  # place at the top
        self.header_frame.grid_columnconfigure(0, weight=1)  # make the header expandable

        # Header label
        self.header_label = ctk.CTkLabel(self.header_frame, text="Welcome", font=('Arial', 16, 'bold'), pady=20)
        self.header_label.grid(row=0, column=0, sticky='nsew')

        # Container for all pages (moved down to row 1)
        self.pages_container.grid(row=1, column=0, sticky='nsew')


        # Navigation bar
        self.nav_bar = ctk.CTkFrame(self)
        self.create_nav_bar()
        self.nav_bar.grid_rowconfigure(0, weight=1)
        self.nav_bar.grid(row=2, column=0, sticky='ns')


        self.show_page("MainPage")


    def show_page(self, page_name):
        '''Show a frame for the given page name and update header text'''
        page = self.pages[page_name]
        page.tkraise()
        # Use the display name from the mapping
        display_name = self.page_display_names.get(page_name, page_name)
        self.header_label.configure(text=display_name)

    def create_nav_bar(self):
        buttons_info = {
            "Vyber aplikacie": "MainPage",
            "SubPage 1": "SubPage1",
            "SubPage 2": "SubPage2",
            "SubPage 3": "SubPage3",
            "SubPage 4": "SubPage4",
            "SubPage 5": "SubPage5"
        }
        col_num = 0
        for text, page_name in buttons_info.items():
            button = ctk.CTkButton(self.nav_bar, text=text, command=lambda name=page_name: self.show_page(name))
            button.configure(font=("Arial", 12))
            button.grid(row=0, column=col_num, padx=10, pady=20, sticky="nsew")
            col_num += 1  # Increment counter for each button
