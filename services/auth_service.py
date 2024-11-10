from services.data_service import get_connection, open_cursor, close_cursor, close_connection

import os
import bcrypt


# Getting database schema from .env
schema = os.environ.get("SCHEMA")




## Login Functions ##

# These functions are used when logging into an account


# Returns user id of user with specified email address
def get_user_id(cursor, email):
    
    try:
        # Searches for users with specified email address
        select_users = f"""
            SELECT id
            FROM {schema}.users
            WHERE email = '{email}'
        """

        # Searches for users
        cursor.execute(select_users)

        # Grabs one user
        result = cursor.fetchone()

        # Formats result into dictionary
        result = {
            "user_id": result[0]
        }


        return result

    
    except Exception as e:
        print(e)
        return False
   



# Returns hash and salt of user with specified id
def get_user_hash_user_salt(cursor, user_id):
    
    try:
        # Searches for hashes and salts for user with specified id
        select_user_hash_user_salt = f"""
            SELECT uh.hash, us.salt 
            FROM {schema}.users AS u
            JOIN {schema}.user_hashes AS uh
				ON u.id = uh.user_id
			JOIN {schema}.user_salts AS us
				ON u.id = us.user_id
            WHERE u.id = {user_id}
        """

        # Searches for user hash and salt
        cursor.execute(select_user_hash_user_salt)

        # Grabs one pair
        result = cursor.fetchone()

        # Formats result into dictionary
        result = {
            "hash": result[0], 
            "salt": result[1]
        }


        return result

    
    except Exception as e:
        print(e)






# Authenticates by decrypting stored hash and checking against user input
# Returns True or False
def authenticate_user(email, password):
    
    # Opens connection and cursor
    connection = get_connection()
    cursor = open_cursor(connection)


    try:
        user_id = get_user_id(cursor, email)

        
        if user_id:
            # Retrieves user_id from dictionary
            user_id = user_id["user_id"]
            
            
            user_hash_user_salt = get_user_hash_user_salt(cursor, user_id)

            # Retrieves hash and salt from dictionary
            hash = user_hash_user_salt["hash"]
            salt = user_hash_user_salt["salt"]

            
            # Generates password hash for input password with retrieved salt
            new_hash = bcrypt.hashpw(password.encode("utf-8"), salt = salt)

            
            # Returns True if new hash matches the stored hash
            if new_hash == hash:
                return True
            else:
                return False


    except Exception as e:
        print(e)

    finally:
        close_cursor(cursor)
        close_connection(connection)


## End Login Functions ##




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


## End Create Account Functions ##