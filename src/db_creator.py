class DBMaker:

    @staticmethod
    def create_database(db_name, cur):
        """Создает базу данных"""
        cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
        cur.execute(f'CREATE DATABASE {db_name}')

    @staticmethod
    def create_table_vacancies(cur):
        """Создает таблицу с вакансиями"""
        cur.execute('DROP TABLE IF EXISTS vacancies')
        cur.execute('''CREATE TABLE vacancies(vacancy_id serial PRIMARY KEY,
                    vacancy_name varchar(100),
                    employer_name varchar(50),
                    salary_from integer,
                    salary_to integer,
                    url text,
                    city varchar(50),
                    employer_id smallint,
                    CONSTRAINT fk_employees_employee_id FOREIGN KEY(employer_id) REFERENCES
                    employers(employer_id) ON DELETE CASCADE)''')

    @staticmethod
    def create_table_employers(cur):
        """Создает таблицу с работодателями"""
        cur.execute('DROP TABLE IF EXISTS employers')
        cur.execute('CREATE TABLE employers(employer_id serial PRIMARY KEY,'
                    'employer_name text,'
                    'url text,'
                    'city varchar(50),'
                    'vacancies_count smallint)')

    @staticmethod
    def fill_vacancies_table(cur, vacancy_name, employer_name, salary_from, salary_to, url, city, employer_id):
        """Заполняет таблицу с вакансиями"""
        cur.execute(
            'INSERT INTO vacancies (vacancy_name, employer_name, salary_from, salary_to, url, city, employer_id)'
            'VALUES (%s,%s,%s,%s,%s,%s,%s)',
            (vacancy_name, employer_name, salary_from, salary_to, url, city, employer_id))

    @staticmethod
    def fill_employers_table(cur, employer_name, url, city, vacancies_count):
        """Заполняет таблицу работодателей"""
        cur.execute(
            'INSERT INTO employers (employer_name, url, city, vacancies_count) VALUES (%s, %s, %s, %s)',
            (employer_name, url, city, vacancies_count))
