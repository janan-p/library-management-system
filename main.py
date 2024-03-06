import sqlite3

#print ("Hi")
connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def insert_data():
    pass

def main():
    '''Main function to run the code'''
    
    global connection, cursor
    path = input("Enter the database file name: ")
    path = './' + path

    connect(path)


    connection.commit()
    connection.close()
    return
    

if __name__ == "__main__":
    main()