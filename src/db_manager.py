import psycopg2

from src.config import config


class DBManager:

    def __init__(self):
        self.conf = self.params

    @property
    def params(self):
        """параметры для psycopg2"""
        conf = config()
        conf.update({'dbname': 'ten_employers'})
        return conf

    def start_connection(self):
        """Создает подключение к базе данных"""
        conn = psycopg2.connect(**self.params)
        return conn

    @staticmethod
    def get_companies_and_vacancies_count(cur):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        cur.execute('SELECT employer_name, vacancies_count FROM employers')
        rows = cur.fetchall()
        return rows

    @staticmethod
    def get_all_vacancies(cur):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        cur.execute('SELECT vacancy_name, employer_name, salary_from, salary_to, url FROM vacancies')
        rows = cur.fetchall()
        return rows

    @staticmethod
    def get_avg_salary(cur):
        """Получает среднюю зарплату по вакансиям."""
        cur.execute('SELECT AVG(salary_from + salary_to) AS avg_salary FROM vacancies')
        rows = cur.fetchall()
        return rows

    @staticmethod
    def get_vacancies_with_higher_salary(cur, avg):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        cur.execute(f'SELECT * FROM vacancies '
                    f'WHERE (salary_from + salary_to)/2 >{avg}'
                    f'GROUP BY vacancy_id')
        rows = cur.fetchall()
        return rows

    @staticmethod
    def get_vacancies_with_keyword(cur, key_word):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        cur.execute(f"SELECT * FROM vacancies "
                    f"WHERE vacancy_name LIKE '%{key_word.lower()}%'"
                    f"OR vacancy_name LIKE '%{key_word.capitalize()}%'")
        rows = cur.fetchall()
        return rows
