import os
import boto3
import pymysql
# Database used is AWS RDS and it stores the daily routine tasks with functions of: add task, view task , mark task and remove task  
ENDPOINT = "database-1.czez8vibtguw.ap-south-1.rds.amazonaws.com"
PORT = 3306
USER = "khyati"
REGION = "ap-south-1"
DBNAME = "db1"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

session = boto3.Session(profile_name='default')
client = session.client('rds')

token = client.generate_db_auth_token(
    DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

class TodoList:
    """To Do List Class"""
    def __init__(self):
        """Basic table is created with specified column."""
        try:
            conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca="C:\\Users\\hp\\Downloads\\ap-south-1-bundle.pem")
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS TODO (Task VARCHAR(100),Status VARCHAR(20));""")
            cur.close()
            conn.close()

        except Exception as _:
            print("Unable to Create a TODO List")

    def add_task(self, task_name):
        """This function adds the feeded task in database and To Do List """
        try:
            conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca="C:\\Users\\hp\\Downloads\\ap-south-1-bundle.pem")
            cur = conn.cursor()
            cur.execute("""INSERT INTO TODO (Task, Status) VALUES (%s, %s)""",(task_name, "Pending"))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as _:
            print("Unable to ADD TASK to the list")

    def view_tasks(self):
        """This function is used to view tasks with their current status"""
        try:
            conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca="C:\\Users\\hp\\Downloads\\ap-south-1-bundle.pem")
            cur = conn.cursor()
            cur.execute("""SELECT COUNT(*) FROM TODO;""")
            row_count = cur.fetchone()[0]

            if row_count == 0 :
                print("No Task Available!!")
            else:
                cur.execute("""SELECT * FROM TODO;""")
                rows = cur.fetchall()

                for row in rows:
                    print(row)

            cur.close()
            conn.close()
        except Exception as _:
            print("Unable to view the Tasks in the TO-DO list")

    def mark_completed(self, task_name):
        """This function is used to mark the task as COMPLETED"""
        try:
            conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca="C:\\Users\\hp\\Downloads\\ap-south-1-bundle.pem")
            cur = conn.cursor()
            cur.execute("""SELECT * FROM TODO WHERE Task = %s;""",(task_name))
            rows = cur.fetchall()

            if len(rows) > 0:
                cur.execute("""UPDATE TODO SET Status = %s WHERE Task = %s;""",("Completed", task_name))
                conn.commit()
            else:
                print("Invalid Task or No such Task Exist!")
            cur.close()
            conn.close()
        except Exception as _:
            print("Unable to mark the Task as Completed!")

    def remove_completed_tasks(self):
        """This function removes all completed Tasks from the To Do List"""
        try:
            conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca="C:\\Users\\hp\\Downloads\\ap-south-1-bundle.pem")
            cur = conn.cursor()
            cur.execute("""DELETE FROM TODO WHERE Status = %s;""",("Completed"))
            conn.commit()
            cur.close()
            conn.close()
            print("All Completed Tasks have been Removed!")
        except Exception as _:
            print("Unable to remove Completed Task.")

def main():
    """The Main Function"""
    todolist = TodoList()
    while True:
        print("\n---------------- To Do List ------------------")
        print("1.   Add Task")
        print("2.   View Task")
        print("3.   Mark Task")
        print("4.   Remove Completed Task")
        print("5.   Close")

        choice = input("Enter Your Choice from 1-5 : ")

        if choice == '1':
            task_name = input("Enter Task Name: ")
            todolist.add_task(task_name)
        elif choice == '2':
            todolist.view_tasks()
        elif choice == '3':
            task_name = input("Enter the task Name: ")
            todolist.mark_completed(task_name)
        elif choice == '4':
            todolist.remove_completed_tasks()
        elif choice == '5':
            print("Thanks for using To do list system\n")
            try:
                conn =  pymysql.connect(host=ENDPOINT, user=USER, passwd=token, port=PORT, database=DBNAME, ssl_ca="C:\\Users\\rahul\\Downloads\\ap-south-1-bundle.pem")
                cur = conn.cursor()
                cur.execute("""SELECT COUNT(*) FROM TODO;""")
                row_count = cur.fetchone()[0]
                cur.close()

                if row_count == 0 :
                    cur = conn.cursor()
                    cur.execute("""DROP TABLE IF EXISTS TODO;""")

                cur.close()
                conn.close()
                break
            except Exception as _:
                print("Unable to delete the empty todo list")

        else:
            print("Invalid option ..... Please Try Again")

if __name__ == '__main__':
    main()