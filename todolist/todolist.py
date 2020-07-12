from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=date.today())

    # def __repr__(self):
    #     return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def print_tasks(tasks, message="Nothing to do!", with_deadline=False):
    if len(tasks) != 0:
        for i, task in enumerate(tasks):
            optional = task.deadline.strftime('%d %b') if with_deadline else ''
            print(f"{i + 1}. {task.task}{optional}")
    else:
        print(message)


def show_today_tasks():
    today = date.today()
    tasks = session.query(Task).filter(Task.deadline == today).all()
    print(f"\nToday {today.strftime('%d %b')}:")
    print_tasks(tasks)
    print()


def show_week_tasks():
    today = date.today()

    for i in range(7 - today.weekday()):
        deadline = today + timedelta(days=i)
        tasks = session.query(Task).filter(Task.deadline == deadline).all()
        print(f'{deadline.strftime("%A %d %b")}:')
        print_tasks(tasks)
        print()


def show_missed_tasks():
    tasks = session.query(Task).filter(Task.deadline < date.today()).all()
    print("\nMissed tasks:")
    print_tasks(tasks, message="Nothing is missed!", with_deadline=True)
    print()


def show_all_tasks():
    tasks = session.query(Task).order_by(Task.deadline).all()
    print("All tasks:")
    print_tasks(tasks, with_deadline=True)
    print()


def add_task():
    task_text = input("\nEnter task\n")
    deadline_str = input("Enter deadline\n")
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
    # print(deadline)
    new_task = Task(task=task_text, deadline=deadline)
    session.add(new_task)
    session.commit()
    print("The task has been added!\n")


def delete_task():
    tasks = session.query(Task).order_by(Task.deadline).all()
    print_tasks(tasks, message="Nothing to delete!", with_deadline=True)
    num = int(input("Chose the number of the task you want to delete:\n"))
    task_to_delete = tasks[num - 1]
    session.delete(task_to_delete)
    session.commit()
    print("The task has been deleted!")


COMMANDS = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit"""

while True:
    print(COMMANDS)
    command = input()
    if command == '1':
        show_today_tasks()
    elif command == '2':
        show_week_tasks()
    elif command == '3':
        show_all_tasks()
    elif command == '4':
        show_missed_tasks()
    elif command == '5':
        add_task()
    elif command == '6':
        delete_task()
    elif command == '0':
        print("\nBye!")
        break
