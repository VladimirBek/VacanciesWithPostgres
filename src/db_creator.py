import json
from configparser import ConfigParser

import psycopg2


class DBMaker:

    def __init__(self):
        self.params = self.config

    @property
    def employers_ids(self):
        with open('employers_ids.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    @property
    def config(self, filename="database.ini", section="postgresql"):
        parser = ConfigParser()
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(
                'Section {0} is not found in the {1} file.'.format(section, filename))
        return db

    def update_config(self, new: dict):
        return self.params.update(new)

    def create_database(self, db_name):
        conn = psycopg2.connect(**self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE {db_name}')
            cur.execute(f'CREATE DATABASE {db_name}')
        conn.commit()
        conn.close()

    @staticmethod
    def create_table_vacancies(cur):
        cur.execute(
            f'''DROP TABLE IF EXISTS vacancies;
                CREATE TABLE vacancies(
                vacancy_id serial PRIMARY KEY,
                vacancy_name varchar(100),
                employer_name varchar(50),
                salary_from integer,
                salary_to integer,
                address text,
                city varchar(50),
                employer_id smallint
            )'''
        )

    @staticmethod
    def create_table_employers(cur):
        cur.execute(
            f'''DROP TABLE IF EXISTS employers;
                CREATE TABLE employers(
                employer_id serial PRIMARY KEY,
                employer_name varchar(100),
                address text,
                city varchar(50),
                vacancies_count smallint
                    )'''
        )

    @staticmethod
    def fill_vacancies_table(cur, vacancy_name, employer_name, salary_from, salary_to, address, city, employer_id):
        cur.execute(
            f'''INSERT INTO vacancies (vacancy_name, salary_from, salary_to, address, city, employer_id)
                VALUES ( 
                {vacancy_name},
                {employer_name} 
                {salary_from}, 
                {salary_to},
                {address},
                {city},
                {employer_id});'''
        )

    @staticmethod
    def fill_employers_table(cur, employer_name, address, city, vacancies_count):
        cur.execute(
            f'''INSERT INTO vacancies (employer_name, address, city, vacancies_count)
                        VALUES ( 
                        {employer_name}, 
                        {address}, 
                        {city},
                        {vacancies_count};'''
        )
