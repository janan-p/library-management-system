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

    cursor.execute('SELECT * FROM members WHERE email=? AND passwd=?', (email, pwd))
    user_data = cursor.fetchone()
    connection.commit()
    if user_data:
        print(f"Sign up successful. Welcome, {user_data[2]}!")
        return email
    else:
        return False 

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
    connection.commit()

    if user_data:
        print(f'Login is successful. Welcome, {user_data[2]}!')
        return email
    
    else:
        print("Invalid email or password.") #We should add a \n at the start of this print statement
        return False 
    
#-----------------------------------------------------------------------------------------------------
        
def member_profile(email):
    # do we need the login to return the email so that we can use it here? maybe add it as a parameter
    #Personal information (such as name, email and birth year).
    #The number of the books they have borrowed and returned (shown as previous borrowings), the current borrowings which is the number of their unreturned borrowings, and overdue borrowings, which is the number of their current borrowings that are not returned within the deadline. The return deadline is 20 days after the borrowing date.
    #Penalty information, displaying the number of unpaid penalties (any penalty that is not paid in full), and the user's total debt amount on unpaid penalties.

    cursor.execute('SELECT email, name, byear FROM members WHERE email=?', (email,))
    member_info = cursor.fetchone() 
    print(f"\nPersonal Information for {member_info[1]}:\n")
    print(f"Email: {member_info[0]}")
    print(f"Birth Year: {member_info[2]}")

    print(f"Borrowings/Returns:")
    cursor.execute(''' 
                    SELECT COUNT(*)  
                    FROM borrowings 
                    WHERE member = ? 
                    AND end_date IS NOT NULL; 
                    ''', (email,))
    
    user_previous_borrowings = cursor.fetchone()[0]
    print(f"Previous borrowings: {user_previous_borrowings} ")

    cursor.execute(''' 
                    SELECT COUNT(*)  
                    FROM borrowings 
                    WHERE member = ? 
                    AND end_date IS NULL; 
                    ''', (email,))
    
    user_current_borrowings = cursor.fetchone()[0]
    print(f"Current borrowings: {user_current_borrowings} ")

    cursor.execute(''' 
                    SELECT COUNT(*)  
                    FROM borrowings 
                    WHERE member = ? 
                    AND end_date IS NULL
                    AND (JULIANDAY(end_date) - JULIANDAY(start_date) > 20); 
                    ''', (email,))
    
    user_overdue_borrowings = cursor.fetchone()[0]
    print(f"Overdue borrowings: {user_overdue_borrowings} ")

    print(f"Penalties:")
    cursor.execute(''' 
                    SELECT COUNT(*)  
                    FROM penalties p 
                    JOIN borrowings b ON p.bid = b.bid
                    WHERE b.member = ? 
                    AND p.amount > p.paid_amount; 
                    ''', (email,))
    
    user_unpaid_penalties = cursor.fetchone()[0]
    print(f"Unpaid penalties: {user_unpaid_penalties} ")

    cursor.execute(''' 
                    SELECT SUM(p.amount - p.paid_amount)  
                    FROM penalties p 
                    JOIN borrowings b ON p.bid = b.bid
                    WHERE b.member = ? 
                    AND p.amount > p.paid_amount; 
                    ''', (email,))
    
    user_total_debt = cursor.fetchone()[0]
    print(f"Total debt on unpaid penalties: {user_total_debt} ")

    pass

def return_a_book(email):
    # work in progress by Janan
    global connection, cursor

    # Borrowing info for books already returned that weren't overdue
    borrowings_query_returned_books = '''
                                      SELECT b.bid AS "Borrowing ID", 
                                             bk.title AS "Book Title",
                                             b.start_date AS "Borrowing Date"
                                      FROM borrowings b, books bk
                                      WHERE b.book_id = bk.book_id
                                      AND b.member = ?
                                      AND b.end_date != NULL
                                      AND (JULIANDAY(b.end_date) - JULIANDAY(b.start_date) <= 20)
                                      '''
    # Borrowing info for books that haven't been returned or were returned late
    borrowings_query_unreturned_books = '''
                                        SELECT b.bid AS "Borrowing ID", 
                                               bk.title AS "Book Title", 
                                               b.start_date AS "Borrowing Date", 
                                               DATE(julianday(b.start_date) + 20) AS "Deadline"
                                        FROM borrowings b, books bk
                                        WHERE b.book_id = bk.book_id
                                        AND b.member = ?
                                        AND (b.end_date = NULL
                                        OR (JULIANDAY(b.end_date) - JULIANDAY(b.start_date) > 20))
                                        '''
    cursor.execute(borrowings_query_returned_books, (email))
    user_returned_borrowings = cursor.fetchall()
    cursor.execute(borrowings_query_unreturned_books, (email))
    user_unreturned_borrowings = cursor.fetchall()
    
    print("%-16s %-16s %-16s %-16s" % ("Borrowing ID", "Book Title", "Borrowing Date", "Deadline")) # Header
    # Print out borrowing info for returned and not overdue books
    for borrowing1 in user_returned_borrowings:
        bid = borrowing1[0]
        title = borrowing1[1]
        borrow_date = borrowing1[2]
        print("%-16s %-16s %-16s" % (bid, title, borrow_date))
    # Print out borrowing info for for unreturned books or were returned late
    for borrowing2 in user_unreturned_borrowings:
        bid = borrowing2[0]
        title = borrowing2[1]
        borrow_date = borrowing2[2]
        deadline = borrowing2[3]
        print("%-16s %-16s %-16s %-16s" % (bid, title, borrow_date, deadline))

    # Execute returning procedure
    print("\nPlease choose a book to return.")
    return_id = input("Borrowing ID: ")

    # Enter today's date as return date in database
    cursor.execute('UPDATE borrowings SET end_date = JULIANDAY("now") WHERE bid = ?', return_id)

    # For overdue borrowings, apply penalty and update in database
    cursor.execute('SELECT start_date, end_date, JULIANDAY(end_date) - JULIANDAY(start_date) AS difference FROM borrowings WHERE bid = ?', return_id)
    returned_book = cursor.fetchone()
    penalty = returned_book[2] - 20
    cursor.execute('UPDATE penalties SET amount = :penalty WHERE bid = :return_id', {"penalty":penalty, "return_id":return_id})

def search_a_book(): #Search for a book
    global connection, cursor

    user_keyword = input("Enter a key word to search for: ")#Main keyword we will use
    search_query = '''
                    SELECT bk.book_id, bk.title, bk.author, bk.pyear, AVG(r.rating)
                    FROM books bk, reviews r, borrowings b
                    WHERE bk.book_id LIKE ? OR bk.author LIKE ?'''#How do we check if the book is available?

def pay_a_penalty():
    pass

#--------------------------------------------------------------------------------------------------------
def main(): 
    global connection, cursor
    path = input("Enter the database file name: ")
    path = './' + path
    connect(path)

    option_choosen = True
    
    current_user = None 
    
    while option_choosen: 
        if current_user == None:
            user_option = input("\nDo you have an account? (Yes or No)\nIf you want to exit (exit): ")

            if user_option.lower() == "exit":#exiting the code
                break

            elif user_option.lower() == "yes" or user_option.lower() == "y": #User already has account, then sign them in
                login_success = login()
                if login_success:
                    #add whatever functions we want the user to perform after they login 
                    current_user = login_success  #return email from login() function
                    
                else:
                    print("Login unsuccessful. Try again or sign up.")
                    continue 
            
            elif user_option.lower() == "no" or user_option.lower() == "n": #User does not have account, sign them up
                signup_success = signup()
                if signup_success:
                    current_user = signup_success
            else:
                print("\nInvalid input! Type either 'yes', 'no', or 'exit'.\n")
                
        else: # there is already a user logged in
            print('\n----------------------------MENU---------------------------\n')
            print('Tasks Available:')
            print('[1]       Member Profile')
            print('[2]       Return a Book')
            print('[3]       Search for Book')
            print('[4]       Pay a Penalty')
            print('[Exit]    To exit Menu')
            print('[Log out] Log out of user')
            
            user_task_choice = input('Choose a task (1,2,3,4,exit,log out): ')
            
            if user_task_choice == '1': #user chose member profile
                member_profile(current_user)

            elif user_task_choice == '2': #user chose return a book
                return_a_book(current_user)

            elif user_task_choice == '3': #user chose search a book
                search_a_book()

            elif user_task_choice == '4': #user chose pay a penalty
                pay_a_penalty()

            elif user_task_choice.lower() == 'log out':
                current_user = None #no current user anymore, as logged out 
                print("Session ended. You have been logged out.")

            elif user_task_choice.lower() == 'exit':
                print('Goodbye, have a good day!')
                break 
                
            else:
                print('Invalid input! Please enter either (1,2,3,4,exit,log out)')
             
    connection.commit()
    connection.close() 
    return

if __name__ == "__main__":
    main()
