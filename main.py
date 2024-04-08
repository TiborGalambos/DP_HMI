import socket


from AppMainLayout import AppMainLayout
from DatabaseManager import DatabaseManager

HOST = 'localhost'
PORT = 65432


if __name__ == "__main__":
    dbm = DatabaseManager()
    # if dbm.check_internet():
    #     dbm.update_coordinates()


    app = AppMainLayout()
    app.mainloop()

