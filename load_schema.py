import sqlite3

def create_database(conn):
	create_table_student = '''CREATE TABLE student (
		id INTEGER PRIMARY KEY,
		first_name TEXT,
		last_name TEXT
	);'''

	create_table_quiz = '''CREATE TABLE quiz (
		id INTEGER PRIMARY KEY,
		subject TEXT,
	    number_of_questions INTEGER,
	    date_taken DATE
	);'''

	create_table_student_quiz = '''CREATE TABLE student_quiz_results (
		id INTEGER PRIMARY KEY,
	    student_id INTEGER,
	    quiz_id INTEGER,
		score INTEGER
	);'''

	cur = conn.cursor()

	cur.execute(create_table_student)
	cur.execute(create_table_quiz)
	cur.execute(create_table_student_quiz)

	conn.commit()

def create_connection(db_file):
	conn = sqlite3.connect(db_file)
	return conn

def create_student(conn, data):
	sql = '''INSERT INTO student
			(id, first_name, last_name)
            VALUES
            (?, ?, ?)'''

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

def create_quiz(conn, data):
	sql = '''INSERT INTO quiz
			(id, subject, number_of_questions, date_taken)
            VALUES
            (?, ?, ?, ?)'''

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

def create_student_quiz(conn, data):
	sql = '''INSERT INTO student_quiz_results
			(id, student_id, quiz_id, score)
            VALUES
            (?, ?, ?, ?)'''

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

def main():
	conn = create_connection("hw13.db")

	create_database(conn)

	Students = [
		(1, 'John', 'Smith')
	]

	Quizzes = [
		(1, 'Python Basics', 5, '2015-02-05')
	]

	Student_Quizzes = [
		(1, 1, 1, 85)
	]

	for student in Students:
		create_student(conn, student)

	for quiz in Quizzes:
		create_quiz(conn, quiz)

	for student_quiz in Student_Quizzes:
		create_student_quiz(conn, student_quiz)

	conn.close()

if __name__ == '__main__':
	main()
