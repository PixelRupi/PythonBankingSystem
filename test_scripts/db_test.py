import mariadb
import sys


def dataBaseConnClose():
    dataBaseCursor.close()
    dataBaseConnection.close()

# laczenie z baza danych
try:
    dataBaseConnection = mariadb.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        port=3306,
        database="bazinga"
    )
except mariadb.Error as mariadbError:
    print(f"a zes odjebal: {mariadbError}")
    sys.exit(1)


# cursor do wykonywania polecen wyciagania danych
dataBaseCursor = dataBaseConnection.cursor()




# insertowanie danych do bazy, takze z uzyciem kursora
'''
try:
    dataBaseCursor.execute("INSERT into logbook_py (callsign, freq, band, mode, grid, comment) values (?, ?, ?, ?, ?, ?);", ("ja9akr", "14200", "20m", "SSB", "as85", ""))
    dataBaseConnection.commit()
except mariadb.Error as mariadbError:
    print(f"a zes odjebal: {mariadbError}")
    sys.exit(1)
'''


# fetchowanie danych z tabeli
try: 
    dataBaseCursor.execute("select * from logbook_py where callsign=?;", ('sq6kpo',))
    # uwierzcie mi, ten przecinek na koncu jest BAAAAARDZO WAZNY                 /|\
    querryResult = dataBaseCursor.fetchall()

    for wiersz in querryResult:
        print(wiersz)
except mariadb.Error as mariadbError:
    print(f"a zes odjebal: {mariadbError}")
    sys.exit(1)


# na pozegnanie
dataBaseConnClose();