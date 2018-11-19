#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

STUDENTS = (
	(1, 'John', 'Smith')
)

QUIZZES = (
	(1, 'Python Basic', 5, '2018-02-05')
)

RESULTS = (
	('1', '1', '85' )
)


con = sqlite3.connect('hw13.db')

with con:

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS STUDENTS")
    cur.execute("CREATE TABLE STUDENTS(ID INTEGER PRIMARY KEY," 
                "FIRST_NAME TEXT NOT NULL, LAST_NAME TEXT NOT NULL)")
    cur.execute("INSERT INTO STUDENTS VALUES(?, ?, ?)", STUDENTS)
    
    cur.execute("DROP TABLE IF EXISTS QUIZZES")
    cur.execute("CREATE TABLE QUIZZES(ID INTEGER PRIMARY KEY NOT NULL, SUBJECT TEXT,"
                "NUM_QUESTIONS INTEGER, QUIZ_DATE TEXT)")
    cur.execute("INSERT INTO QUIZZES VALUES(?, ?, ?, ?)", QUIZZES)
    
    cur.execute("DROP TABLE IF EXISTS RESULTS")
    cur.execute("CREATE TABLE RESULTS(STUD_ID INTEGER NOT NULL, QUIZ_ID INTEGER NOT NULL,"
                "SCORE INTEGER NOT NULL)")
    cur.execute("INSERT INTO RESULTS VALUES(?, ?, ?)", RESULTS)
