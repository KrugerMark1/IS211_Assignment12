from flask import Flask, render_template, request, Response, redirect, url_for, session
import re
import json
from random import randrange
import sqlite3

app = Flask(__name__)
app.secret_key = 'COMPUTERSCIENCE'

def create_student(conn, data):
	sql = '''INSERT INTO student
			(first_name, last_name)
            VALUES
            (?, ?)'''

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

def create_quiz(conn, data):
	sql = '''INSERT INTO quiz
			(subject, number_of_questions, date_taken)
            VALUES
            (?, ?, ?)'''

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

def create_student_quiz(conn, data):
	sql = '''INSERT INTO student_quiz_results
			(student_id, quiz_id, score)
            VALUES
            (?, ?, ?)'''

	cur = conn.cursor()
	cur.execute(sql, data)
	conn.commit()

def select_students(conn):
	cur = conn.cursor()
	cur.execute('SELECT * FROM student')

	rows = cur.fetchall()

	print(rows)

	return(rows)

def select_quizzes(conn):
	cur = conn.cursor()
	cur.execute('SELECT * FROM quiz')

	rows = cur.fetchall()

	print(rows)

	return(rows)

def select_quizzes_by_student_id(conn, sid):
	cur = conn.cursor()
	cur.execute('SELECT * FROM student_quiz_results WHERE student_id=?', (sid,))

	rows = cur.fetchall()
	return(rows)

@app.route('/student/add', methods=['GET', 'POST'])
def student_add():
	if session.get('auth'):
		if request.method == 'GET':
			messages = request.args.get('messages')
			return(render_template('student_add.html', error_messages=messages))

		elif request.method == 'POST':
			args = request.form

			student = (args.get('first'), args.get('last'))

			conn = sqlite3.connect('hw13.db')

			try:
				create_student(conn, student)
				conn.close()
			except:
				return(redirect(url_for('.student_add', messages="Error. Please try again.")))

			return(redirect('/dashboard'))

	else:
		return(redirect('/login'))

@app.route('/student/<sid>')
def student_by_id(sid):
	if session.get('auth'):
		conn = sqlite3.connect('hw13.db')
		quizzes = select_quizzes_by_student_id(conn, sid)
		conn.close()
		return(render_template('student_quizzes.html', quizzes=quizzes))
	else:
		return(redirect('/login'))

@app.route('/results/add', methods=['GET', 'POST'])
def results_add():
	if session.get('auth'):
		if request.method == 'GET':
			messages = request.args.get('messages')
			conn = sqlite3.connect('hw13.db')
			students = select_students(conn)
			quizzes = select_quizzes(conn)
			conn.close()

			return(render_template('results_add.html', 
				students=students,
				quizzes=quizzes,
				error_messages=messages))

		elif request.method == 'POST':
			args = request.form
			student_quiz = (args.get('student'), args.get('quiz'), args.get('score'))
			conn = sqlite3.connect('hw13.db')

			try:
				create_student_quiz(conn, student_quiz)
				conn.close()
			except:
				conn.close()
				return(redirect(url_for('.results_add', messages="Error. Please try again.")))

			return(redirect('/dashboard'))

	else:
		return(redirect('/login'))

@app.route('/quiz/add', methods=['GET', 'POST'])
def quiz_add():
	if session.get('auth'):
		if request.method == 'GET':
			messages = request.args.get('messages')
			return(render_template('quiz_add.html', error_messages=messages))

		elif request.method == 'POST':
			args = request.form

			quiz = (args.get('subject'), args.get('num'), args.get('date'))

			conn = sqlite3.connect('hw13.db')

			try:
				create_quiz(conn, quiz)
				conn.close()
			except:
				return(redirect(url_for('.quiz_add', messages="Error. Please try again.")))

			return(redirect('/dashboard'))

	else:
		return(redirect('/login'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
	if session.get('auth'):
		conn = sqlite3.connect('hw13.db')
		students = select_students(conn)
		quizzes = select_quizzes(conn)
		conn.close()
		return(render_template('dashboard.html', 
				students=students,
				quizzes=quizzes))
	else:
		return(redirect('/login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

	if request.method == 'GET':
		messages = request.args.get('messages')
		return(render_template('login.html', error_messages=messages))

	elif request.method == 'POST':

		args = request.form

		login_details = {
		  "username": args.get('username'),
		  "password": args.get('password')
		}

		if login_details.get('username') == 'admin' and login_details.get('password') == 'password':
			session['auth'] = True
			return(redirect('/dashboard'))
		else:
			session['auth'] = False
			return(redirect(url_for('.login', messages="Error. Incorrect Login Credentials.")))

if __name__ == '__main__':
	app.run()