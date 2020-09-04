# Write your code here
from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


main_menu = ['1) Today\'s tasks', '2) Week\'s tasks', '3) All tasks',
             '4) Missed tasks', '5) Add task', '6) Delete task', '0) Exit']

no_task = 'Nothing to do!\n'

def menu(menu_items):
    _ = [print(item) for item in menu_items]
    n = int(input('> ' ))
    print('')
    return n


def today_tasks():
    today = datetime.today()
    print('Today {} {}:'.format(today.day, today.strftime('%b')))
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print_tasks(rows)


def print_tasks(rows):
    tasks = [row.task for row in rows]
    if len(tasks) == 0:
        print(no_task)
    else:
        _ = [print('{}. {}'.format(i, item)) for i, item in enumerate(tasks, 1)]
        print('')


def print_tasks_time(rows):
    if len(rows) == 0:
        print(no_task)
    else:
        _ = [print('{}. {}. {} {}'.format(i, row.task, row.deadline.day, row.deadline.strftime('%b'))) for i, row in
             enumerate(rows, 1)]
        print('')

def add_task():
    new_task = input('Enter task\n')
    new_deadline = datetime.strptime(input('Enter deadline (YYYY-MM-DD)\n'), '%Y-%m-%d')
    new_row = Table(task = new_task, deadline = new_deadline)
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')


def week_tasks():
    today = datetime.today()
    for i in range(7):
        nextdate = today + timedelta(days=i)
        print('{} {} {}:'.format(nextdate.strftime("%A"), nextdate.day, nextdate.strftime('%b')))
        rows = session.query(Table).filter(Table.deadline == nextdate.date()).all()
        print_tasks(rows)


def all_tasks():
    print('All tasks:')
    rows = session.query(Table).order_by(Table.deadline).all()
    print_tasks_time(rows)

def missed_tasks():
    print('Missed tasks:')
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    print_tasks_time(rows)

def delete_task():
    print('Choose the number of the task you want to delete:')
    rows = session.query(Table).order_by(Table.deadline).all()
    print_tasks_time(rows)
    n = int(input('> '))
    session.delete(rows[n - 1])
    session.commit()
    print('The task has been deleted!\n')

while True:
    n = menu(main_menu)
    if n == 0:
        break
    if n == 1:
        today_tasks()
    elif n == 2:
        week_tasks()
    elif n == 3:
        all_tasks()
    elif n == 4:
        missed_tasks()
    elif n == 5:
        add_task()
    elif n == 6:
        delete_task()

print('Bye!')

# todo_list = ['Do yoga', 'Make breakfast', 'Learn basics of SQL', 'Learn what is ORM']
#
# print('Today:')
# _ = [print('{}) {}'.format(i + 1, todo_list[i])) for i in range(len(todo_list))]