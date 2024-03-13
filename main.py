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
    print(f"\n--------- Personal Information for {member_info[1]}: ---------\n")
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

    print(f"\n-------------- Penalties: --------------\n")
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
    global connection, cursor

    # Borrowing info for books that haven't been returned (including overdues)
    borrowings_query_unreturned_books = '''
                                        SELECT b.bid AS "Borrowing ID", 
                                               bk.title AS "Book Title", 
                                               b.start_date AS "Borrowing Date", 
                                               DATE(julianday(b.start_date) + 20) AS "Deadline"
                                        FROM borrowings b, books bk
                                        WHERE b.end_date IS NULL
                                        AND b.book_id = bk.book_id
                                        AND b.member = ?
                                        '''
    cursor.execute(borrowings_query_unreturned_books, (email,))
    user_borrowings = cursor.fetchall()

    if not user_borrowings:
        print("\nYou do not have any borrowings!")
    else:
        print("\n%-16s %-16s %-16s %-16s" % ("Borrowing ID", "Book Title", "Borrowing Date", "Deadline")) # Header
        # Print out borrowing info for unreturned books
        for borrowing in user_borrowings:
            bid = borrowing[0]
            title = borrowing[1]
            borrow_date = borrowing[2]
            deadline = borrowing[3]
            print("%-16s %-16s %-16s %-16s" % (bid, title, borrow_date, deadline))

        # Check if the return_id chosen by the user is valid
        print("\nPlease choose a book to return.")
        return_id = input("Borrowing ID: ")

        found = False
        while not found:
            for borrowing2 in user_borrowings:
                if int(borrowing2[0]) == int(return_id):
                    found = True
                    break
            if not found:
                print("\nPlease enter a valid BID to return.")
                return_id = input("Borrowing ID: ")

        # Enter today's date as return date in database
        cursor.execute('UPDATE borrowings SET end_date = JULIANDAY("now") WHERE bid = ?', (return_id,))

        print("\nYour book is successfully returned!")

        '''
        
        Do we want to add a section that tells the user that they returned a book late and a penalty was applied?
        
        '''

        # For overdue borrowings, apply penalty and update in database
        cursor.execute('SELECT start_date, end_date, JULIANDAY(end_date) - JULIANDAY(start_date) AS difference FROM borrowings WHERE bid = ?', (return_id,))
        returned_book = cursor.fetchone()
        penalty = returned_book[2] - 20
        cursor.execute('UPDATE penalties SET amount = :penalty WHERE bid = :return_id', {"penalty":penalty, "return_id":return_id})

        # Optional review
        review_option = input("\nWould you like to write a review? (Yes or No): ")
        while review_option.lower() != "yes" and review_option.lower() != "y" and review_option.lower() != "no" and review_option.lower() != "n":
            review_option = input("\nInvalid input! Type either 'yes' or 'no': ")

        if review_option.lower() == "yes" or review_option.lower() == "y":
            review_text = input("\nWhat is your review for this book? \n")
            review_rating = input("\nWhat rating would you give this book? (1-5 inclusive) ")
            while int(review_rating) < 1 or int(review_rating) > 5:
                print("\nPlease enter a number between 1 to 5 inclusive.")
                review_rating = input("\nWhat rating would you give this book? (1-5 inclusive) ")

            # Find last rid number
            cursor.execute('SELECT rid FROM reviews ORDER BY rid DESC LIMIT 1')
            last_rid = cursor.fetchone()

            # Get value of book_id for the current borrowing
            cursor.execute('SELECT book_id FROM borrowings WHERE bid = ?', (return_id,))
            book_id = cursor.fetchone()
            
            # Add user's review into review table
            review_query = '''
                        INSERT INTO reviews VALUES(:rid, :book_id, :member, :rating, :rtext, JULIANDAY("now")) 
                        '''
            cursor.execute(review_query, {"rid":last_rid[0] + 1, "book_id":book_id[0], "member":email, "rating":review_rating, "rtext":review_text})
    
    connection.commit()

def search_a_book(email): #Search for a book
    global connection, cursor

    user_keyword = input("Enter a key word to search for: ").lower()#Main keyword we will use
    title_query = '''
                    SELECT bk.book_id, bk.title, bk.author, bk.pyear, IFNULL(AVG(r.rating), 'No Rating'),
                    Case 
                        When br.end_date IS NULL then 'unavailble'
                        When exists (select 1
                                    from borrowings br
                                    where br.book_id = bk.book_id)
                                    then 'Unavialble'
                    Else 'Available' End

                    FROM books bk
                    LEFT JOIN reviews r ON bk.book_id = r.book_id
                    LEFT JOIN borrowings br on bk.book_id = br.book_id
                    WHERE bk.title LIKE '%'||?||'%' 
                    GROUP BY bk.book_id
                    ORDER BY bk.title ASC; 
                    '''#How do we check if the book is available? When br.end_date IS NULL then 'Unavailable'
                    #Never been borrowed
                    #Already been returned - end_date is before current date
    
    # Case 
    #                     When br.end_date IS NULL then 'unavailble'
    #                     When exists (select 1
    #                                 from borrowings br
    #                                 where br.book_id = bk.book_id)
    #                                 then 'Unavialble'
    #                 Else 'Available' End
  
#BORROWING TABLE 
# 1|arch@ualberta.ca|1|2023-11-15|
# 2|arch@ualberta.ca|2|2023-11-15|
# 3|siddh@ualberta.ca|3|2023-11-15|
# 4|keya@ualberta.ca|4|2023-10-15|2023-10-25
# 5|keya@ualberta.ca|5|2023-10-15|2023-10-25
# 6|dhiya@ualberta.ca|6|2023-10-15|2023-11-25
# 7|annoying@ualberta.ca|4|2023-10-15|2023-11-25
# 8|dhanshri@ualberta.ca|5|2023-10-15|2023-10-25
# 9|jpanchal@ualberta.ca|6|2023-11-15|
# 10|asshah1@ualberta.ca|7|2023-11-15|
    cursor.execute(title_query, (user_keyword,)) 
    title_list = cursor.fetchall()
    # print(title_list)
    print("\nMatching Title List:")
    for book in title_list:
        book_id, title, author, pyear, rating, avail = book
        print(f'{book_id} {title} {author} {pyear} {rating} {avail}')

    author_query = '''
                    SELECT bk.book_id, bk.title, bk.author, bk.pyear, IFNULL(AVG(r.rating), 'No Rating'),
                    CASE
                        WHEN (br.end_date IS NULL OR EXISTS (SELECT 1 FROM borrowings br WHERE br.book_id = bk.book_id))
                            AND NOT (br.end_date IS NULL AND EXISTS (SELECT 1 FROM borrowings br WHERE br.book_id = bk.book_id)) THEN 'Available'
                        ELSE 'Unavialable'
                    END
                    FROM books bk
                    LEFT JOIN reviews r ON bk.book_id = r.book_id
                    LEFT JOIN borrowings br on bk.book_id = br.book_id
                    WHERE bk.author LIKE '%'||?||'%'
                    GROUP BY bk.book_id;
                    '''
    cursor.execute(author_query, (user_keyword,)) 
    author_list = cursor.fetchall()
    print("\nMatching Author list:")
    for author in author_list:
        book_id, title, author, pyear, rating, available= author
        print(f'{book_id} {title} {author} {pyear} {rating} {available}')
    connection.commit()
    return

def pay_a_penalty(email):
    '''
    Displays users unpaid fees anf give them an option to pay partially or fully.
    '''
    global connection, cursor

    # Find the user's penalties
    penalty_query = '''
                    SELECT p.pid, p.amount, IFNULL(p.paid_amount, 0) 
                    FROM penalties p, borrowings b 
                    WHERE b.member = ?
                    AND b.bid = p.bid
                    AND (p.paid_amount IS NULL OR p.paid_amount < p.amount)
                    '''
    cursor.execute(penalty_query, (email,))
    unpaid_penalties = cursor.fetchall()

    # if the user has no penalties
    if len(unpaid_penalties) == 0:
        print("\nYou do not have any unpaid penalties!")
        return
    
    # show all the unpaid penalties
    for penalty in unpaid_penalties:
        pid, amount, paid_amount = penalty
        print(f"\nPenalty ID: {pid}, Amount: {amount}, Paid Amount: {paid_amount}")

    # make sure the penalty ID is valid and set the penalty they want to pay as chosen penalty
    valid_id = False
    while not valid_id:
        chosen_pid = int(input("Enter the Penalty ID to pay: "))
        for penalty in unpaid_penalties:
            if penalty[0] == chosen_pid:
                chosen_penalty = penalty
                valid_id = True
                break
        if not valid_id:
            print("Invalid Penalty ID. Please try again.")

    chosen_pid = chosen_penalty[0]
    print(f"You have chosen Penalty # {chosen_penalty[0]}, the fee is {chosen_penalty[1]}, and you have paid {chosen_penalty[2]}.")
    
    # Calcuate remainin penalty fee so user can't pay more than they need to
    if paid_amount is None:
        remaining_amount = chosen_penalty[1]
    else:
        remaining_amount = chosen_penalty[1] - chosen_penalty[2]
    #print(remaining_amount)
    # User can partially or fully pay   
    payment = float(input("Enter amount you want to pay: "))
    if payment <= remaining_amount:
        paid_amount = payment + chosen_penalty[2]
        payment_query = '''
                    UPDATE penalties SET paid_amount = ? WHERE pid = ?
                    '''      
        cursor.execute(payment_query, (paid_amount, chosen_pid))
        connection.commit()
        print("Payment Successful.")
    else:
        print("Payment exceeds the remaining amount. Payment not processed.")
        
    return
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
                search_a_book(current_user)

            elif user_task_choice == '4': #user chose pay a penalty
                pay_a_penalty(current_user)

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