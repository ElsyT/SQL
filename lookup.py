import sqlite3
import json
import xml.etree.ElementTree as ET
try:
    conn = sqlite3.connect("HyperionDev.db") # read file for user to connect
    cur = conn.cursor()
    with open('create_database.sql', 'r' ) as sql_file:
        sql_commds = sql_file.read() 
    commands = sql_commds.split (';')
    for command in commands:
        cur.execute(command)
    conn.commit()
except sqlite3.Error as e:
    print(e)
    print("Please store your database as HyperionDev.db")
    quit()



def usage_is_incorrect(input, num_args): # for incorrect input
    if len(input) != num_args + 1:
        print(f"The {input[0]} command requires {num_args} arguments.")
        return True
    return False

def store_data_as_json(data, filename): # save as json
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def store_data_as_xml(data, filename): # save as XMl  file
    root = ET.Element("data")
    for item in data:
     record = ET.Element("record")
     for key, value in item.items():
        field = ET.Element(key)
        field.text = str(value)
        record.append(field)
        root.append(record)
    tree = ET.ElementTree(root)
    tree.write(filename)
  


def offer_to_store(data): # offers to the the store as json / xml file
   
    while True:
        print("Would you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()

        if choice == "y":
            filename = input("Specify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1]
            if ext == 'xml':
                store_data_as_xml(data, filename)
                break  # 
            elif ext == 'json':
                store_data_as_json(data, filename)
                break
            else:
                print("Invalid file extension. Please use .xml or .json")

        elif choice == 'n':
            break

        else:
            print("Invalid choice")

usage = '''
What would you like to do?

d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")

while True:
    print()
    # Get input from user
    user_input = input(usage).split(" ")
    print()

    # Parse user input into command and args
    command = user_input[0]
    if len(user_input) > 1:
        args = user_input[1:]

    if command == 'd': # demo this prints all student names and surnames 
        data = cur.execute("SELECT * FROM Student")
        for _, firstname, surname, _, _ in data:
            print(f"{firstname} {surname}")
        
    elif command == 'vs': # view subjects by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        query = "SELECT c.course_name FROM StudentCourse sc INNER JOIN Course c ON sc.course_code = c.course_code WHERE sc.student_id = ?"
        column_names = ["course_name"]
        data = cur.execute(query, (student_id,)).fetchall()
        if data :
            for row in data:
                print(row[0])
        else:
            print(f"No subjects found for the student ID {student_id}")
        data = [{'course_name': row[0]} for row in data]
        # Run SQL query and store in data
        offer_to_store(data)
        

    elif command == 'la':# list address by name and surname
        if usage_is_incorrect(user_input, 2):
            continue
        firstname, surname = args[0], args[1]
        query = "SELECT street, city FROM Address INNER JOIN Student ON Address.address_id = Student.address_id WHERE first_name = ? AND last_name = ? "
        column_names = ["street", "city"]
        data = cur.execute(query, (firstname,surname)).fetchall()
        if data :
            for row in data:
                print(row[0:1])
        else:
            print (f"No such Student found for {firstname,surname}")
        data = [{'course_name': row[0:1]} for row in data]
        offer_to_store(data)
        pass
    
    elif command == 'lr':# list reviews by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        query = "SELECT completeness, efficiency, style, documentation, review_text FROM Review WHERE student_id = ? " #only noticed now its eacher id will submit the correct format promptly
        column_names = [",completeness", "efficiency", "style", "documentation", "review_text"]
        data = cur.execute(query, (student_id,)).fetchall()
        if data :
            for row in data:
                print(row[0:5])
        else :
            print (f"No Review found for the Student id {student_id}")
        data = [{'course_name': row[0:5]} for row in data]
        # Run SQL query and store in data
        offer_to_store(data)

    elif command == 'lc':# list reviews by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        teacher_id = args[0]
        query = "SELECT * FROM Course WHERE teacher_id = ? " #only noticed now but  lc is on the panel but not in the instructions
        column_names = ["course_code", "course_name ", "course_description", "teacher_id", "course_level "]
        data = cur.execute(query, (teacher_id,)).fetchall()
        if data :
            for row in data:
                print(row[0:5])
        else :
            print (f"No Review found for the Student id {student_id}")
        data = [{'course_name': row[0:5]} for row in data]
        # Run SQL query and store in data
        offer_to_store(data)
        pass
        
    
    elif command == 'lnc':# list all students who haven't completed their course
        
        query= "SELECT Student.student_id, first_name, last_name, email  FROM Student INNER JOIN StudentCourse ON Student.student_id = StudentCourse.student_id WHERE is_complete = 0"
        data = cur.execute(query).fetchall()
        column_names = ["student_id", "first_name", "last_name", "email"]
        if data :
            for row in data:
                print(row[0:4])
        else:
            print("All students have completed they work!")
        data = [{'course_name': row[0:4]} for row in data]

        offer_to_store(data)
        
    
    elif command == 'lf':# list all students who have completed their course and got a mark <= 30
    
        query = "SELECT Student.student_id, first_name, last_name, email FROM Student INNER JOIN StudentCourse ON Student.student_id = StudentCourse.student_id WHERE mark <= 30 and is_complete = 1"
        column_names = ["student_id", "first_name", "last_name", "email"]
        data = cur.execute(query).fetchall()
        if data :
            for row in data:
                print(row[0:4])
        else:
            print("All students have donr a good job!")
        data = [{'course_name': row[0:4]} for row in data]

        offer_to_store(data)
        
    
    elif command == 'e':
        
        query = " SELECT Address.street, Address.city , Student.first_name , Student.last_name FROM Address INNER JOIN Student ON Address.address_id = Student.address_id  "  
        column_names = [ "first_name", "last_name", "city", "state"]
        data = cur.execute(query).fetchall()  
        if data:
            for row in data:
                print(row)
        print("Program exited successfully!")
        break
    
    else:
        print(f"Incorrect command: '{command}'")
conn.close()
