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

def login(): #logs the user in or signs them up
    global connection, cursor

    option_choosen = True
    user_id = ''

    while option_choosen == True:
        user_option = input("\nDo you have an account? (Yes or no) \n If you want to exit (exit).\n")

        if user_option.lower() == "exit":#exiting the code
            quit()

        if user_option.lower() == "yes" or user_option.lower() == "y": #User already has account, then sign them in
            pass
        elif user_option.lower() == "no" or user_option.lower() == "n": #User does not have account, sign them up
            pass
        else:
            print("\nInvalid input! Type either 'Yes' or 'No'\n")


def insert_data():
    pass

def main():
    '''Main function to run the code'''

    global connection, cursor
    path = input("Enter the database file name: ")
    path = './' + path

    connect(path)
    login()

    connection.commit()
    connection.close()
    return
    

if __name__ == "__main__":
    main()