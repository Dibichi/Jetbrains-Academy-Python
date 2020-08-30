import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Specifies the properties of the table that is to be created
class TaskTable(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

# Accesses the database and creates table
def create_table():
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base.metadata.create_all(engine) # creates table after being defined by TaskTable
    Session = sessionmaker(bind=engine)
    return Session()


class TaskManager:
    global session
    today = datetime.today()

    # Prints the main menu
    def main_menu(self):
        print('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
        ''')

    # Determines how the table will be printed based on what arguments are passed
    def print_tasks(self, row_tasks, custom_txt, optional_txt=False):

        # Prints custom text for when there are no tasks
        if len(row_tasks) == 0:
            print(custom_txt)

        # Prints the date next to the task
        elif optional_txt is True:
            for num, task in enumerate(row_tasks, start=1):
                format_date = task.deadline.strftime('%#d %b')
                print('{}. {}. {}'.format(num, task, format_date))

        else:
            for num, task in enumerate(row_tasks, start=1):
                print(f'{num}. {task}')


    # Adds a specified task and deadline to the list / table
    def add_task(self):
        user_task = input('Enter task\n')
        user_deadline = input('Enter deadline\n')
        new_task = TaskTable(task=user_task, deadline=datetime.strptime(user_deadline, '%Y-%m-%d').date())
        session.add(new_task)
        session.commit()
        print('The task has been added!\n')

    # View all tasks on the table / list
    def view_tasks(self):
        all_tasks = session.query(TaskTable).order_by(TaskTable.deadline).all()
        print('All tasks:')
        self.print_tasks(all_tasks, 'Nothing to do!', True)

    # View all the tasks for today - filters table for today, prints header, then prints the tasks of today
    def view_today(self):
        today_rows = session.query(TaskTable).filter(TaskTable.deadline == self.today.date()).all()
        print('Today {}:'.format(self.today.strftime('%d %b')))
        self.print_tasks(today_rows, 'Nothing to do!')

    # View all the tasks from today to next week
    def view_week(self):
        next_week = self.today + timedelta(days=7)
        week_day = self.today

        # Loops through every day until it is next week - prints date header then prints tasks for that date
        while week_day != next_week:
            print('{}:'.format(week_day.strftime('%A %d %b')))
            weekday_rows = session.query(TaskTable).filter(TaskTable.deadline == week_day.date()).all()
            self.print_tasks(weekday_rows, 'Nothing to do!')
            print('\n')
            week_day = week_day + timedelta(days=1)

    # Checks for any tasks that are before today's date
    def missed_tasks(self):
        missing_rows = session.query(TaskTable).filter(TaskTable.deadline < self.today.date()).all()
        print('Missed tasks')
        self.print_tasks(missing_rows, 'Nothing is missed!', True)

    # Deletes the selected task if there are any from the table / list
    def delete_task(self):
        print('Choose the number of the task you want to delete')
        all_tasks = session.query(TaskTable).order_by(TaskTable.deadline).all()
        self.print_tasks(all_tasks, 'Nothing is missed!', True)
        if len(all_tasks) != 0:
            user_delete = int(input('\n'))
            session.delete(all_tasks[user_delete - 1])
            session.commit()
            print('The task has been deleted')


session = create_table()
manager = TaskManager()
user_actions = {1: manager.view_today, 2: manager.view_week, 3: manager.view_tasks, 4: manager.missed_tasks, 5: manager.add_task, 6: manager.delete_task}
while True:
    manager.main_menu()
    user_input = int(input())

    if user_input == 0:
        print('Bye!')
        exit()

    # All actions that can be performed on the todo list
    elif user_input in user_actions:
        user_actions[user_input]()

    else:
        print('Invalid input!')
