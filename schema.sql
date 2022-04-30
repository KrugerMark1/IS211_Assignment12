CREATE TABLE student (
	id INTEGER PRIMARY KEY,
	first_name TEXT,
	last_name TEXT
);

CREATE TABLE quiz (
	id INTEGER PRIMARY KEY,
	subject TEXT,
    number_of_questions INTEGER,
    date_taken DATE
);

CREATE TABLE student_quiz_results (
	id INTEGER PRIMARY KEY,
    student_id INTEGER,
    quiz_id INTEGER,
	score INTEGER
);