import pymysql
from pymongo import MongoClient
from datetime import date
import base64
import os

# MySQL connection
mysql_conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='student_management_system'
)

print('Connected to MySQL!')


# MongoDB connection
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['student_management_system']

print('Connected to MongoDB!')



# Fetch data from MySQL, transform, and insert into MongoDB
def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

gender_map = {1: 'Female', 0: 'Male'}


def get_image_base64(student_id):
    img_path = os.path.join('ProfilePicture', f'{student_id}.png')
    if os.path.exists(img_path):
        with open(img_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

with mysql_conn.cursor() as cursor:
    cursor.execute('SELECT * FROM student;')
    for row in cursor.fetchall():
        # Assuming row = (id, F_name, L_name, dob, gender)
        mysql_id, f_name, l_name, dob, gender = row
        image_b64 = get_image_base64(mysql_id)
        doc = {
            '_id': mysql_id,
            'Name': f_name + l_name,
            'age': calculate_age(dob),
            'gender': gender_map.get(gender, 'Other'),
            'image': image_b64
        }
        print('Inserting to MongoDB:', doc)
        mongo_db['student'].replace_one({'_id': mysql_id}, doc, upsert=True)



# Fetch and print data from MongoDB
for doc in mongo_db['student'].find().limit(5):
    print('MongoDB Document:', doc)

# Close connections
mysql_conn.close()
mongo_client.close()
