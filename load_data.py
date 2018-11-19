#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

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
	('1', '2', '65' ),
	('1', '4', '85' ),
	('1', '1', '90' ),
	('1', '3', '75' ),
	('1', '5', '65' ),
	('2', '2', '55' ),
	('2', '4', '89' ),
	('2', '1', '78' ),
	('2', '3', '92' ),
	('2', '5', '88' ),
	('3', '2', '85' ),
	('3', '4', '87' ),
	('3', '1', '69' ),
	('3', '3', '77' ),
	('3', '5', '90' ),
	('4', '2', '61' ),
	('4', '4', '87' ),
	('4', '1', '68' ),
	('4', '3', '70' ),
	('4', '5', '93' ),
	('5', '2', '66' ),
	('5', '4', '69' ),
	('5', '1', '87' ),
	('5', '3', '85' ),
	('5', '5', '90' )
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
