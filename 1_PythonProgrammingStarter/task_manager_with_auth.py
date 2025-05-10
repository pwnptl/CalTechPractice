import csv
import hashlib
import os
import random

credentials_file_name = 'credentials.csv'
tasks_folder = 'tasks\\'

credentials_dict = {}
task_list = []
task_loaded = False
logged_in_user_name = None


def load_credentials():
    global credentials_dict
    try:
        with open(credentials_file_name, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username_hash = row['username_hash']
                password_hash = row['password_hash']
                credentials_dict[username_hash] = password_hash
            file.flush()
    except FileNotFoundError:
        pass


def load_tasks():
    global task_list
    global logged_in_user_name
    if logged_in_user_name is None:
        return
    try:
        task_file_name = tasks_folder + logged_in_user_name + '.csv'
        with open(task_file_name, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                task_list.append(row)
            file.flush()
    except FileNotFoundError:
        pass


def save_tasks():
    global task_list
    global logged_in_user_name
    if logged_in_user_name is None:
        return
    try:
        os.makedirs(tasks_folder, exist_ok=True)
        task_file_name = tasks_folder + logged_in_user_name + '.csv'
        fieldnames = ['task_id', 'description', 'status']
        with open(task_file_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for task in task_list:
                writer.writerow(task)
                file.flush()
                os.fsync(file.fileno())
    except FileNotFoundError:
        print('file not found', task_file_name)
        pass
    pass


def append_credential_in_store(username_hash, password_hash):
    global credentials_dict
    try:
        fieldnames = ['username_hash', 'password_hash']
        file_exists = os.path.exists(credentials_file_name)
        with open(credentials_file_name, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({'username_hash': username_hash, 'password_hash': password_hash})
            file.flush()
            os.fsync(file.fileno())
    except FileNotFoundError:
        pass
    credentials_dict[username_hash] = password_hash
    pass


def attempt_login():
    global logged_in_user_name
    while True:
        try:

            username = input("--------> Enter Usernmame : ")
            if username == '':
                return
            password = input('--------> Enter password : ')

            username_hash = _hash(username)
            password = _hash(password)
            if username_hash in credentials_dict and credentials_dict[username_hash] == password:
                logged_in_user_name = username
                load_tasks()
                print('logged in with user : ', logged_in_user_name)
                break
        except ValueError:
            continue
    pass


def _hash(param):
    return hashlib.sha256(param.encode()).hexdigest()
    pass


def create_account():
    while True:
        print('-----> Lets create your account')
        username = input('Enter username:')
        if username == '':
            return
        password = input('Enter password:')
        repeat_pass = input('Repeat password:')
        if password == repeat_pass:
            username_hash = _hash(username)
            password_hash = _hash(password)
            if username_hash in credentials_dict:
                print('username exists, retrying')
                continue
            append_credential_in_store(username_hash, password_hash)
            return
    pass


pre_login_menu_dict = [  # indexing assume from 1
    (1, "1. Login", attempt_login),
    (2, "2. Create Account", create_account),
    (3, "3. Exit", None)
]


def get_pre_login_operation_from_menu():
    while True:
        try:
            print('------------------------------')
            for menu_item in pre_login_menu_dict:
                print(menu_item[1])
            choice = int(input("----------> Enter Choice : "))
            if 1 <= choice <= len(pre_login_menu_dict):
                return pre_login_menu_dict[choice - 1][2]
        except ValueError:
            print('please enter a valid number.')
            continue


def generate_random_id(min_id, max_id):
    return random.randint(min_id, max_id)


def create_task_id():
    min_id = 11
    max_id = 20
    while True:
        for i in range(5):
            random_id = generate_random_id(min_id, max_id)
            is_present = False
            for task in task_list:
                if task['task_id'] == random_id:
                    is_present = True
                    break
            if is_present:
                continue
            return random_id
        min_id = max_id + 1
        max_id = max_id * 10
    pass


def create_task():
    description = input('Enter Task Description : ')
    task_id = create_task_id()
    status = 'pending'

    task = {'task_id': task_id,
            'description': description,
            'status': status}
    print(task)
    task_list.append(task)


def view_tasks():
    print('-------------Viewing Tasks------------------------------------')
    print("{:<3} {:<5} {:<40} {:<12}".format("#", "id", "Description", "Status"))
    for index, task in enumerate(task_list, start=1):
        print("{:<3} {:<5} {:<40} {:<12}".format(
            index,
            task['task_id'],
            task['description'],
            task['status'],
        ))

    print('--------------------------------------------------------------')


def logout():
    save_tasks()
    global logged_in_user_name
    logged_in_user_name = None
    global task_list
    task_list = []


def complete_task():
    id = input("Enter id to mark complete : ")
    for task in task_list:
        if task['task_id'] == id:
            task['status'] = 'complete'
            print('marked task', task['task_id'], 'complete: ', task['description'])
            return
    print('task', task['task_id'], 'not found')

    pass


def delete_task():
    id = input("Enter id to delete : ")
    for task in task_list:
        if task['task_id'] == id:
            task_list.remove(task)
            return
    pass


post_login_menu_dict = [  # indexing assume from 1
    (1, "1. Create Task", create_task),
    (2, "2. View tasks", view_tasks),
    (3, "3. Mark Task as Completed", complete_task),
    (3, "4. Delete Task", delete_task),
    (3, "5. Logout", logout)
]


def get_post_login_operation():
    while True:
        try:
            print('------------------------------')
            for menu_item in post_login_menu_dict:
                print(menu_item[1])
            choice = int(input("----------> Enter Choice : "))
            if 1 <= choice <= len(post_login_menu_dict):
                return post_login_menu_dict[choice - 1][2]
        except ValueError:
            print('please enter a valid number.')
            continue


if __name__ == '__main__':
    load_credentials()

    while True:
        if logged_in_user_name is None:
            operation = get_pre_login_operation_from_menu()
        else:
            operation = get_post_login_operation()

        if operation is None:
            break
        operation()
