import pymysql

# Connect to the MySQL database
conn = pymysql.connect(
    host='user_db',
    user='sql_user',
    password='password',
    database='user_db'
)

cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute("SELECT * FROM users where email = \"{}\" and password = \"{}\" ".format("Harsh@example.com","1234"))
# Fetch the result
result = cursor.fetchall()

print(len(result))
print(result)