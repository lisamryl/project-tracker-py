"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print "Student: {first} {last}\nGitHub account: {acct}".format(
        first=row[0], last=row[1], acct=row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
        INSERT INTO students (first_name, last_name, github)
          VALUES (:first_name, :last_name, :github)
        """

    db.session.execute(QUERY, {'first_name': first_name,
                               'last_name': last_name,
                               'github': github})
    db.session.commit()

    print "Successfully added student: {first} {last}".format(
        first=first_name, last=last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""

    QUERY = """
        SELECT title, description, max_grade
        FROM projects
        WHERE title = :title
        """

    db_cursor = db.session.execute(QUERY, {'title': title})

    row = db_cursor.fetchone()

    print "Project: {title} - Max Grade: {max_grade}\n{description}".format(
        title=row[0], description=row[1], max_grade=row[2])


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """
            SELECT student_github, project_title, grade
            FROM grades
            WHERE student_github = :github AND project_title = :title"""

    db_cursor = db.session.execute(QUERY, {'github': github, 'title': title})

    row = db_cursor.fetchone()

    print "Student received {grade} on Project {title}.".format(
        grade=row[2], title=row[1])


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""

    QUERY = """
        INSERT INTO grades (grade, student_github, project_title)
        VALUES (:grade, :github, :title)
    """

    db.session.execute(QUERY, {'grade': grade,
                               'github': github,
                               'title': title})

    db.session.commit()

    print "Successfully added student grade."


def add_project(title, description, max_grade):
    """Add a new project to the project table in the database."""

    QUERY = """
            INSERT INTO projects (title, description, max_grade)
            VALUES (:title, :description, :max_grade)
    """

    db.session.execute(QUERY, {
        'title': title,
        'description': description,
        'max_grade': max_grade})

    db.session.commit()

    print "Successfully added project {} into database.".format(title)


def get_grades_by_github_title(github):
    """Print grade student received for a project."""
    QUERY = """
            SELECT student_github, project_title, grade
            FROM grades
            WHERE student_github = :github"""

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchall()

    for item in row:
        print "Student received {grade} on Project {title}.".format(
        grade=item[2], title=item[1])


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            title = args[0]
            get_project_by_title(title)

        elif command == "grade":
            github = args[0]
            title = args[1]
            get_grade_by_github_title(github, title)

        elif command == "assign_grade":
            student, project_title, grade = args
            assign_grade(student, project_title, grade)

        elif command == "add_project":
            title = args[0]
            project_title = " ".join(args[1:-1])
            max_grade = args[-1]
            add_project(title, project_title, max_grade)

        else:
            if command != "quit":
                print "Invalid Entry. Try again."


if __name__ == "__main__":
    connect_to_db(app)

    # handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
