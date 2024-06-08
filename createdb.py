import mysql.connector
from mysql.connector import errorcode

try:
    my_db = mysql.connector.connect(
        host="localhost",
        user="omar",
        password="mansaring",
        auth_plugin='mysql_native_password'  # Specify the auth plugin
    )

    my_cursor = my_db.cursor()
    
    # Create the database if it does not exist
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS Nzavote")

    print("Database 'Nzavote' created successfully or already exists.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    if my_db.is_connected():
        my_cursor.close()
        my_db.close()
        print("MySQL connection is closed")
