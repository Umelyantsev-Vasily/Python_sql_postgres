# Исходные данные для заполнения таблиц
import csv
import os

os.makedirs('C:\\tmp', exist_ok=True)
os.environ['TEMP'] = 'C:\\tmp'
os.environ['TMP'] = 'C:\\tmp'


with open(os.path.join('../data', 'customers_data.csv'), newline='', encoding='utf-8') as file:
    customers_data = [row for row in csv.reader(file) if 'customer_id' not in row]

with open(os.path.join('../data', 'employees_data.csv'), newline='', encoding='utf-8') as file:
    employees_data = [row for row in csv.reader(file) if 'first_name' not in row]

with open(os.path.join('../data', 'orders_data.csv'), newline='', encoding='utf-8') as file:
    orders_data = [row for row in csv.reader(file) if 'order_id' not in row]

# Импортируйте библиотеку psycopg2
import psycopg2

# Создайте подключение к базе данных
conn = psycopg2.connect(dbname="test_2", user="postgres", password="221096", port="5432", host="localhost")

# Открытие курсора
cur = conn.cursor()

# Создание таблиц
cur.execute(
    """
    CREATE TABLE customers (
        customer_id char(5) PRIMARY KEY,
        company_name VARCHAR(100) NOT NULL,
        contact_name VARCHAR(100) NOT NULL
    )
"""
)
cur.execute(
    """
    CREATE TABLE employees (
        employee_id int PRIMARY KEY,
        first_name VARCHAR(25) NOT NULL,
        last_name VARCHAR(35) NOT NULL,
        title VARCHAR(100) NOT NULL,
        birth_date DATE,
        notes TEXT
    )
"""
)
cur.execute(
    """
    CREATE TABLE orders (
        order_id int PRIMARY KEY,
        customer_id char(5) REFERENCES customers(customer_id),
        employee_id int REFERENCES employees(employee_id),
        order_date DATE,
        ship_city VARCHAR(100) NOT NULL
    )
"""
)
conn.commit()

# Вставка данных в customers
for data in customers_data:
    if len(data) == 3:
        cur.execute(
            "INSERT INTO customers (customer_id, company_name, contact_name) VALUES (%s, %s, %s) returning *",
            data,
        )
    else:
        print(f"Пропущена строка customers_data: {data} - неверное количество полей")
conn.commit()
res_customers = cur.fetchall()

for idx, data in enumerate(employees_data, start=1):
    if len(data) == 5:
        employee_id = idx
        first_name = data[0]
        last_name = data[1]
        title = data[2]
        birth_date = data[3]
        notes = data[4]

        cur.execute(
            "INSERT INTO employees (employee_id, first_name, last_name, title, birth_date, notes) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
            (employee_id, first_name, last_name, title, birth_date, notes)
        )
    else:
        print(f"Пропущена строка employees_data: {data} - неверное количество полей")
conn.commit()
res_employees = cur.fetchall()

# Вставка данных в orders
for data in orders_data:
    if len(data) == 5:
        cur.execute(
            "INSERT INTO orders (order_id, customer_id, employee_id, order_date, ship_city) VALUES (%s, %s, %s, %s, %s) returning *",
            data,
        )
    else:
        print(f"Пропущена строка orders_data: {data} - неверное количество полей")
conn.commit()
res_orders = cur.fetchall()

# Закрытие курсора
cur.close()
# Закрытие соединения
conn.close()
