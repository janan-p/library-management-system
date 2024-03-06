import sqlite3
import getpass

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def signup():
    '''
    User does not have an account and wants to signup.
    '''
    global connection, cursor
    print("\nTo sign up enter the following information:")
    email = input("Email: ")
    name = input("Name: ")
    byear = input("Birth Year: ")
    faculty = input("Faculty: ")
    pwd = getpass.getpass()
    print("Confirm Password: ")
    pwd2 = getpass.getpass()

    while pwd != pwd2:
        print("Password did not match")
        pwd = getpass.getpass()
        print("Confirm Password: ")
        pwd2 = getpass.getpass()

    insert_query = '''
        INSERT INTO members (email, passwd, name, byear, faculty) 
        VALUES (?, ?, ?, ?, ?)'''
    # cursor.execute(insert_query, (email, pwd, name, byear, faculty))
    print("Password Match! Account had been created.")
    connection.commit()

def login(): #logs the user in or signs them up
    global connection, cursor

    option_choosen = True
    user_id = ''
    
    while option_choosen == True:
        user_option = input("\nDo you have an account? (Yes or no)\nIf you want to exit (exit).\n")

        if user_option.lower() == "exit":#exiting the code
            quit()
        if user_option.lower() == "yes" or user_option.lower() == "y": #User already has account, then sign them in
            pass
        elif user_option.lower() == "no" or user_option.lower() == "n": #User does not have account, sign them up
            signup()
            option_choosen = False
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