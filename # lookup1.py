# lookup.py 


import sqlite3
import json
import xml.etree.ElementTree as ET

# Connect to the database
conn = sqlite3.connect('HyperionDev.db')
cur = conn.cursor()

# Function to save query results to a file in JSON or XML format
def save_results(results, filename, file_format):
    if file_format == 'json':
        with open(filename, 'w') as outfile:
            json.dump(results, outfile)
    elif file_format == 'xml':
        root = ET.Element('results')
        for row in results:
            result = ET.SubElement(root, 'result')
            for i in range(len(row)):
                field = ET.SubElement(result, 'field')
                field.set('name', cur.description[i][0])
                field.text = str(row[i])
        tree = ET.ElementTree(root)
        tree.write(filename)


# Function to display query results on console
def display_results(results, fields):
    for row in results:
        output = ''
        for i in range(len(fields)):
            output += str(row[fields[i]]).ljust(20)  # Adjust the spacing as needed
        print(output)
    print()  # Add an empty line after displaying results


# Query 1: View all subjects being taken by a specified student (search by student_id)
def query1():
    student_id = input("Enter student ID: ")
    cur.execute("SELECT c.course_name FROM Course c JOIN StudentCourse s  on c.course_code=s.course_code WHERE s.student_id=?", (student_id,))
               
               
    results = cur.fetchall()
    display_results(results, [0])
    save = input("Save results to file? (y/n): ")
    if save == 'y':
        filename = input("Enter filename: ")
        format = input("Enter format (json/xml): ")
        save_results(results, filename, format)

# Query 2: Look up an address given a first name and a surname
def query2():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    cur.execute("SELECT a.street, a.city FROM Address a join student s on a.address_id=s.address_id WHERE s.first_name=? AND s.last_name=?", (first_name, last_name))             
    results = cur.fetchall()
    display_results(results, [0, 1])
    save = input("Save results to file? (y/n): ")
    if save == 'y':
        filename = input("Enter filename: ")
        format = input("Enter format (json/xml): ")
        save_results(results, filename, format)

# Query 3: List all reviews given to a student (search by student_id)
def query3():
    student_id = input("Enter student ID: ")
    cur.execute("SELECT completeness, efficiency, style, documentation, review_text FROM review WHERE student_id=?", (student_id,))           
    results = cur.fetchall()
    display_results(results, [0, 1, 2, 3, 4])
    save = input("Save results to file? (y/n): ")
    if save == 'y':
        filename = input("Enter filename: ")
        format = input("Enter format (json/xml): ")
        save_results(results, filename, format)

# Query 4: List all courses being given by a specific teacher (search by teacher_id)
def query4():
    teacher_id = input("Enter teacher ID: ")
    cur.execute("SELECT course_name FROM Course WHERE teacher_id=?", (teacher_id,))
    results = cur.fetchall()
    display_results(results, [0])
    save = input("Save results to file? (y/n): ")
    if save == 'y':
        filename = input("Enter filename: ")
        format = input("Enter format (json/xml): ")
        save_results(results, filename, format)

# Query 5: List all students who haven’t completed their course
def query5():
    cur.execute("SELECT s.student_id, st.first_name, st.last_name, st.email, c.course_name from StudentCourse s INNER JOIN Course c ON s.course_code=c.course_code LEFT OUTER JOIN Student st ON st.student_id= s.student_id WHERE s.is_complete=0;")
    results = cur.fetchall()
    display_results(results, [0, 1, 2, 3, 4])
    save = input("Save results to file? (y/n): ")
    if save == 'y':
        filename = input("Enter filename: ")
        format = input("Enter format (json/xml): ")
        save_results(results, filename, format)

# Query 6: List all students who have completed their course and achieved a mark of 30 or below
def query6():
    cur.execute("SELECT s.student_id, st.first_name, st.last_name, st.email, c.course_name from StudentCourse s INNER JOIN Course c ON s.course_code=c.course_code LEFT OUTER JOIN Student st ON st.student_id= s.student_id WHERE s.is_complete= 1 AND mark<=30;")
    results = cur.fetchall()
    display_results(results, [0, 1, 2, 3, 4])
    save = input("Save results to file? (y/n): ")
    if save == 'y':
        filename = input("Enter filename: ")
        format = input("Enter format (json/xml): ")
        save_results(results, filename, format)

# Main program loop
while True:
    print("What would you like to do?:")
    print("vs. View all subjects being taken by a specified student")
    print("la. Look up an address given a first name and a surname")
    print("lr. List all reviews given to a student")
    print("lc. List all courses being given by a specific teacher")
    print("lnc. List all students who haven’t completed their course")
    print("lf. List all students who have completed their course and achieved a mark of 30 or below")
    print("e. Exit")
    choice = input("Enter your choice: ")
    if choice == 'vs':
        query1()
    elif choice == 'la':
        query2()
    elif choice == 'lr':
        query3()
    elif choice == 'lc':
        query4()
    elif choice == 'lnc':
        query5()
    elif choice == 'lf':
        query6()
    elif choice == 'e':
        break
    else:
        print("Invalid query.")
    print('-------------------------------------------------')
        
        
# Close the database connection
conn.close()