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

    cursor.execute('SELECT email FROM members WHERE email=?', (email))
    if cursor.fetchone():
        print("This email is already registered. Try signing up with a new email.")
        return
    
    name = input("Name: ")
    byear = input("Birth Year: ")
    faculty = input("Faculty: ")
    pwd = getpass.getpass("Password: ")
    pwd2 = getpass.getpass("Confirm Password: ")

    while pwd != pwd2:
        print("Password did not match.")
        pwd = getpass.getpass("Password: ")
        pwd2 = getpass.getpass("Confirm Password: ")

    insert_query = '''
        INSERT INTO members (email, passwd, name, byear, faculty) 
        VALUES (?, ?, ?, ?, ?)'''
    
    cursor.execute(insert_query, (email, pwd, name, byear, faculty))
    print("Password Match! Account had been created.")
    connection.commit()

def login(): #logs the user in or signs them up
    global connection, cursor

    option_choosen = True
    user_id = ''
    
    while option_choosen == True: #maybe we can keep this part in the main?
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

def login_maybe():

    global connection, cursor
    print ("\nPlease enter your email and password.")
    
    email = input("Email: ")
    password = getpass.getpass("Password: ")

    cursor.execute('SELECT * FROM members WHERE email=? AND passwd=?', (email, password))
    user_data = cursor.fetchone()

    if user_data:
        print("Login is successful. Welcome, ", user_data[2])
        return True
    
    else:
        print("Invalid email or password.")
        return False 
    

def main_maybe(): 

    global connection, cursor
    path = input("Enter the database file name: ")
    path = './' + path

    connect(path)

    option_choosen = True
    
    while option_choosen == True: 

        user_option = input("\nDo you have an account? (Yes or no)\nIf you want to exit (exit).\n")

        if user_option.lower() == "exit":#exiting the code
            break

        elif user_option.lower() == "yes" or user_option.lower() == "y": #User already has account, then sign them in
            login_success = login_maybe()
            if login_success:
                #add whatever functions we want the user to perform after they login 
                break

        elif user_option.lower() == "no" or user_option.lower() == "n": #User does not have account, sign them up
            signup()

        else:
            print("\nInvalid input! Type either 'yes', 'no', or 'exit'.\n")

    connection.commit()
    connection.close()     

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
