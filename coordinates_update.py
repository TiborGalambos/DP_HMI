from Managers.DatabaseManager import DatabaseManager

if __name__ == "__main__":
    dbm = DatabaseManager()
    for i in range (2):
        print(i)
    if dbm.check_internet():
        dbm.update_coordinates()