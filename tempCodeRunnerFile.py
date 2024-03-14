review_rating = input("\nWhat rating would you give this book? (1-5 inclusive) ")
            while int(review_rating) < 1 or int(review_rating) > 5:
                print("\nPlease enter a number between 1 to 5 inclusive.")
                r