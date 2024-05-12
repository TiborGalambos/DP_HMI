from Pages.AppMainLayout import AppMainLayout
from Managers.DatabaseManager import DatabaseManager

# HOST = 'localhost'
# PORT = 65432

if __name__ == "__main__":
    dbm = DatabaseManager()

    app = AppMainLayout()
    app.mainloop()

