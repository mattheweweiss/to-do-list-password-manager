from services.data_service import get_connection, open_cursor, close_cursor, close_connection

import os
import bcrypt


# Getting database schema from .env
schema = os.environ.get("SCHEMA")



## Create Account Functions ##

# These functions are used when an account is being created


# Searches if email address is in user table
# Used to reject account creation if email is already in-use
# Returns True or False
def find_user(email):


    # Opens connection and cursor
    connection = get_connection()
    cursor = open_cursor(connection)


    try:
        # Searches for users with specified email address
        select_users = f"""
            SELECT *
            FROM {schema}.users
            WHERE email = '{email}'
        """

        # Searches for users
        cursor.execute(select_users)

        # Grabs one user
        result = cursor.fetchone()

    
    except Exception as e:
        print(e)
        # Does not allow user to be created
        return True
        
    finally:
        close_cursor(cursor)
        close_connection(connection)

    
    # Returns true if user is found, returns false otherwise
    if result:
        return True
    else:
        return False




# Creates user and user hash and user salt and stores in database
def create_user(first_name, last_name, email, password):

    
    # Initializing user_rows as 0
    user_rows = 0


    # Opens connection and cursor
    connection = get_connection()
    cursor = open_cursor(connection)

    
    try:
        
        # Generates unique salt
        salt = bcrypt.gensalt(rounds = 15)


        # Generates password hash with salt
        hash = bcrypt.hashpw(password.encode("utf-8"), salt = salt)


        # Decodes the salt and hash to insert into tables
        salt = salt.decode()
        hash = hash.decode()


        insert_user = f"""
            INSERT INTO {schema}.users (
                first_name
                ,last_name
                ,email
            ) VALUES (
                '{first_name}'
                ,'{last_name}'
                ,'{email}'
            )
        """


        # Inserts user into users table
        cursor.execute(insert_user)


        # Grabs the ID of the inserted user
        user_id = cursor.lastrowid


        # Query to insert hash -- needed user ID
        insert_hash = f"""
            INSERT INTO {schema}.user_hashes (
                user_id
                ,hash
            ) VALUES (
                {user_id}
                ,'{hash}'
            )
        """


        # Query to insert salt -- needed user ID
        insert_salt = f"""
            INSERT INTO {schema}.user_salts (
                user_id
                ,salt
            ) VALUES (
                {user_id}
                ,'{salt}'
            )
        """


        # Inserts user hash into user_hashes table
        cursor.execute(insert_hash)
        # Inserts user salt into user_salts table
        cursor.execute(insert_salt)


        user_rows = cursor.rowcount
        print(user_rows)


        connection.commit()

    
    except Exception as e:
        print(e)
        connection.rollback()

    finally:
        close_cursor(cursor)
        close_connection(connection)

    
    return user_rows