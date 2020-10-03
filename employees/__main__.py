from sys import argv

from employees.db.db_employees import EmployeeDb, NotFoundError
from employees.db.db_helper import create_table, save_data
from employees.db.db_manager import DatabaseManager
from employees.config import DB_NAME, DB_USER, DB_PASSWORD
from employees.util import load_data


def init_db():
    """Creates a database and loads data from a json file.
    :param file_path: should be path to data load, default it is '../data.json'
    """
    file_path = argv[1] if argv[1] else "../data.json"

    with DatabaseManager(DB_NAME, DB_USER, DB_PASSWORD) as conn:
        create_table(conn)

        # it is possible to validate json but suppose it is always correct
        data = load_data(file_path)
        save_data(conn, data)

    print('Data loaded successful')


def get_names():
    """Print employees` names by office id.
    :param person_id: should be int and over than 0
    """
    person_id = argv[1]
    if not argv[1].isdigit():
        print('input param should be number')
        exit(1)
    person_id = int(person_id)

    if not person_id > 0:
        print('input param should be over than 0')
        exit(1)

    with DatabaseManager(DB_NAME, DB_USER, DB_PASSWORD) as conn:
        employee_db = EmployeeDb(conn)

        try:
            if not employee_db.is_employee_id(person_id):
                print("input id is not belong to employee")
                exit(1)
        except NotFoundError:
            print(f"employee with id={person_id} is not found")
            exit(1)

        office_id = employee_db.get_office_id(person_id)
        if office_id is None:
            print(f'office with id-{office_id} does not exist')
        else:
            print(employee_db.get_employees(office_id))
