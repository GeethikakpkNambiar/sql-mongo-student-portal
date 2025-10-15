from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['student_management_system']


@app.route('/', methods=['GET', 'POST'])
def index():
    student = None
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        if student_id:
            student = mongo_db['student'].find_one({'_id': student_id})
    return render_template('students.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
