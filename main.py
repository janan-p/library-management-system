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
    has_email = True
    while has_email:
        cursor.execute('SELECT email FROM members WHERE email=?', (email,))
        if cursor.fetchone():
            print("This email is already registered. Try signing up with a new email.")
            email = input("Email: ")
        else:
            has_email = False 
    
    name = input("Name: ")
    byear = input("Birth Year: ")
    faculty = input("Faculty: ")
    pwd = getpass.getpass("Password: ")
    pwd2 = getpass.getpass("Confirm Password: ")
    while pwd != pwd2:
        print("Password did not match.")
        pwd2 = getpass.getpass("Confirm Password: ")
    insert_query = '''
        INSERT INTO members (email, passwd, name, byear, faculty) 
        VALUES (?, ?, ?, ?, ?)'''
    
    cursor.execute(insert_query, (email, pwd, name, byear, faculty))
    print("Password Match! Account had been created.")
    connection.commit()
    return 

def login():
    '''
    Logs the user in by checking if email and password are the same
    '''
    global connection, cursor
    print ("\nPlease enter your email and password.")
    
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    cursor.execute('SELECT * FROM members WHERE email=? AND passwd=?', (email, password))
    user_data = cursor.fetchone()
    if user_data:
        print(f'Login is successful. Welcome, {user_data[2]}')
        return True
    
    else:
        print("Invalid email or password.")
        return False 
#-----------------------------------------------------------------------------------------------------
        
def member_profile():
    pass

def return_a_book():
    pass

def search_a_book():
    pass

def pay_a_penalty():
    pass

#--------------------------------------------------------------------------------------------------------
def main(): 
    global connection, cursor
    path = input("Enter the database file name: ")
    path = './' + path
    connect(path)
    option_choosen = True
    perform_task = False

    while option_choosen == True: 
        user_option = input("\nDo you have an account? (Yes or No)\nIf you want to exit (exit).\n")

        if user_option.lower() == "exit":#exiting the code
            break

        elif user_option.lower() == "yes" or user_option.lower() == "y": #User already has account, then sign them in
            login_success = login()
            if login_success:
                #add whatever functions we want the user to perform after they login 
                perform_task = True
                break
            

        elif user_option.lower() == "no" or user_option.lower() == "n": #User does not have account, sign them up
            signup()
            perform_task = True
            option_choosen = False

        else:
            print("\nInvalid input! Type either 'yes', 'no', or 'exit'.\n")
    
    
    #------------------------------------------------------------------------------------------------------------------------
    while perform_task: #While loop to always ask the user for a task 
        print('\n----------------------------MENU---------------------------\n')
        print('Tasks Available:')
        print('[1]       Member Profile')
        print('[2]       Return a Book')
        print('[3]       Search for Book')
        print('[4]       Pay a Penalty\n')
        print('[Exit]    To exit Menu')
        print('[Log out] Log out of user')
        user_task_choice = input('Choose a task (1,2,3,4,exit,log out): ')
        if user_task_choice == '1': #user chose member profile
            member_profile()

        elif user_task_choice == '2': #user chose return a book
            return_a_book()

        elif user_task_choice == '3': #user chose search a book
            search_a_book()

        elif user_task_choice == '4': #user chose pay a penalty
            pay_a_penalty()

        elif user_task_choice.lower() == 'exit':
            print('Goodbye! Have a good day!')
            perform_task = False

        elif user_task_choice.lower() == 'log out':
            pass
            #HOW DO WE LOG SOMEONE OUT???>?>>?>?>?
            perform_task = False

        else:
            print('Invalid input! Please enter either (1,2,3,4,exit,log out)')


    connection.commit()
    connection.close() 
    return

if __name__ == "__main__":
    main()
