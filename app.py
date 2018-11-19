#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IS211_Assingment13: A simple flask web appilication."""

from flask import Flask, request, redirect, url_for, session, g, abort, render_template, flash
import sqlite3
from contextlib import closing
import os

STUDENTS = (
	(1, 'George', 'Washington'),
	(2, 'Abraham', 'Lincoln'),
	(3, 'Thomas', 'Fefferson'),
	(4, 'Andrew', 'Jackson'),
	(5, 'John', 'Adams')
)

QUIZZES = (
	(1, 'Python Programming', 10, '2018-05-05'),
	(2, 'Data acquisition', 20, '2018-06-10'),
	(3, 'Geographic Info Systems', 12, '2018-07-11'),
	(4, 'Enterprise Resource Planning', 20, '2018-06-20'),
	(5, 'Project Management', 10, '2018-07-05')
)

RESULTS = (
	(1, 2, 65 ),
	(1, 1, 90 ),
	(2, 4, 89 ),
	(2, 5, 88 ),
	(3, 2, 85 ),
	(3, 1, 69 ),
	(4, 1, 68 ),
	(4, 3, 70 ),
	(5, 3, 85 ),
	(5, 5, 90 )
)


con = sqlite3.connect('data.db')

with con:

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS STUDENTS")
    cur.execute("CREATE TABLE STUDENTS(ID INTEGER PRIMARY KEY," 
                "FIRST_NAME TEXT NOT NULL, LAST_NAME TEXT NOT NULL)")
    cur.executemany("INSERT INTO STUDENTS VALUES(?, ?, ?)", STUDENTS)
    
    cur.execute("DROP TABLE IF EXISTS QUIZZES")
    cur.execute("CREATE TABLE QUIZZES(ID INTEGER PRIMARY KEY NOT NULL, SUBJECT TEXT,"
                "NUM_QUESTIONS INTEGER, QUIZ_DATE TEXT)")
    cur.executemany("INSERT INTO QUIZZES VALUES(?, ?, ?, ?)", QUIZZES)
    
    cur.execute("DROP TABLE IF EXISTS RESULTS")
    cur.execute("CREATE TABLE RESULTS(STUD_ID INTEGER NOT NULL, QUIZ_ID INTEGER NOT NULL,"
                "SCORE INTEGER NOT NULL)")
    cur.executemany("INSERT INTO RESULTS VALUES(?, ?, ?)", RESULTS)

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE = 'data.db',
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='test'
))


def connect_db():
    return sqlite3.connect('data.db')


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'data.db', None)
    if db is not None:
        db.close()

        
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Username is incorrect'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Password is incorrect'
        else:
            session['logged_in'] = True
            flash('Log in Successful')
            return redirect('/dashboard')
    return render_template('login.html', error=error)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    cur = g.db.execute('select ID, FIRST_NAME, LAST_NAME from STUDENTS')
    students = [dict(ID=row[0], FIRST_NAME=row[1], LAST_NAME=row[2])
                for row in cur.fetchall()]
    cur1 = g.db.execute('select ID, SUBJECT, NUM_QUESTIONS, QUIZ_DATE from QUIZZES')
    quizzes = [dict(ID=row[0], SUBJECT=row[1], NUM_QUESTIONS=row[2],
                    QUIZ_DATE=row[3]) for row in cur1.fetchall()]
    return render_template('dashboard.html',
                           students=students, 
                           quizzes=quizzes)


@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template('addstudent.html')
    elif request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        g.db.execute('insert into STUDENTS (FIRST_NAME, LAST_NAME) values (?, ?)',
                     [request.form['FIRST_NAME'], request.form['LAST_NAME']])
        g.db.commit()
    flash('New student added')
    return redirect(url_for('dashboard'))


@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'GET':
        return render_template('addquiz.html')
    elif request.method == 'POST':
        if not session.get('logged_in'):
            abort(401)
        g.db.execute('insert into QUIZZES (SUBJECT, NUM_QUESTIONS, QUIZ_DATE) '
                     'values (?, ?, ?)', [request.form['SUBJECT'],
                                          request.form['NUM_QUESTIONS'],
                                          request.form['QUIZ_DATE']])
        g.db.commit()
    flash('New quiz successfully added')
    return redirect(url_for('dashboard'))

@app.route('/student/<id>', methods=['GET'])
def display_results(id):
    cur2 = g.db.execute('select FIRST_NAME, LAST_NAME from STUDENTS where ID = ?', id)
    stu_names = [dict(FIRST_NAME=row[0], LAST_NAME=row[1]) for row in cur2.fetchall()]
    cur3 = g.db.execute('select QUIZ_ID, SCORE '
                        ',QUIZZES.SUBJECT from RESULTS '
                        'left join QUIZZES on RESULTS.QUIZ_ID = QUIZZES.ID '
                        'where STUD_ID = ?', id)
    results = [dict(QUIZ_ID=row[0], SCORE=row[1]
                   ,SUBJECT=row[2]) for row in cur3.fetchall()]
    return render_template('results.html', results=results, stu_names=stu_names)
    

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if request.method == 'GET':
        cur4 = g.db.execute('select ID, SUBJECT from QUIZZES')
        quizzes = [dict(quiz_id=row[0], subject=row[1]) for row in cur4.fetchall()]
        cur5 = g.db.execute('select ID, FIRST_NAME, LAST_NAME from STUDENTS')
        students = [dict(student_id=row[0], student_name='{} {}'.format(row[1], row[2]))
                    for row in cur5.fetchall()]
        return render_template('addresults.html', quizzes=quizzes, students=students)
    elif request.method == 'POST':
        g.db.execute("insert into RESULTS (STUD_ID, QUIZ_ID, SCORE) values "
                     "(?, ?, ?)", (request.form['STUD_ID'],
                                   request.form['QUIZ_ID'], request.form['SCORE']))
        g.db.commit()
        flash("Quiz updated")
        return redirect('/dashboard')
    else:
        flash("Failed to Update Record")
        return redirect('/results/add')

    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Log Out Sucessful')
    return redirect(url_for('login'))


if __name__=='__main__':
    app.run(debug=True, use_reloader=False)
