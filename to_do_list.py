# Write your code here
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today()


def print_tasks(when):
    if when == 'Today':
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        print(f'Today {today.day} {today.strftime("%b")}')
        if not rows:
            print('Nothing to do!')
        else:
            for count, i in enumerate(rows, 1):
                print(count, i, sep='. ')
    elif when == 'Week':
        for x in range(7):
            weekday = today.date() + timedelta(x)
            rows = session.query(Table).filter(Table.deadline == weekday).all()
            print(f'{weekday.strftime("%A")} {weekday.day} {weekday.strftime("%b")}')
            if not rows:
                print('Nothing to do!\n')
            else:
                for count, i in enumerate(rows, 1):
                    print(count, i, '\n', sep='. ')
    elif when == 'All':
        rows = session.query(Table).order_by(Table.deadline).all()
        for count, i in enumerate(rows, 1):
            print(count, i, f'{i.deadline.day} {i.deadline.strftime("%b")}', sep='. ')
    elif when == 'Missed':
        rows = session.query(Table).filter(Table.deadline < today.date()).all()
        print('Missed Tasks:')
        if not rows:
            print('Nothing to do!')
        else:
            for count, i in enumerate(rows, 1):
                print(count, i, f'{i.deadline.day} {i.deadline.strftime("%b")}', sep='. ')


def add_task():
    new_task = input('Enter task: ')
    new_deadline = input('Enter deadline: ')
    new_row = Table(task=new_task, deadline=datetime.strptime(new_deadline, '%Y-%m-%d'))
    session.add(new_row)
    print('The task has been added!')


def delete_task():
    print('Choose the number of the task you want to delete: ')
    rows = session.query(Table).order_by(Table.deadline).all()
    if not rows:
        print('Nothing to delete')
    else:
        for i in rows:
            print(i.id, i, f'{i.deadline.day} {i.deadline.strftime("%b")}', sep='. ')
        delete = input()
        session.query(Table).filter(Table.id == int(delete)).delete()
        print('The task has been deleted!')


while True:
    print("\n1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    choice = input()
    print()
    if choice == '0':
        print('Bye!')
        break
    elif choice == '1':
        print_tasks('Today')
    elif choice == '2':
        print_tasks('Week')
    elif choice == '3':
        print_tasks('All')
    elif choice == '4':
        print_tasks('Missed')
    elif choice == '5':
        add_task()
        session.commit()
    elif choice == '6':
        delete_task()
        session.commit()
