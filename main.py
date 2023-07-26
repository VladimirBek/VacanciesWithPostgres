import json
import os
import psycopg2

from src.config import config
from src.db_creator import DBMaker
from src.hh_api import HHApi


def main():
    hh = HHApi()
    db_creator = DBMaker()
    with open(os.path.join('src', 'employers_ids.json'), 'r', encoding='utf-8') as f:
        ids = json.load(f)

    params = config()
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    db_creator.create_database('ten_employers', conn.cursor())
    conn.cursor().close()
    conn.close()
    params.update({'dbname': 'ten_employers'})
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    with conn.cursor() as cur:
        db_creator.create_table_employers(cur)
        db_creator.create_table_vacancies(cur)
        for employer in ids:
            items = hh.get_emps_vacancies(employer)
            for item in items:
                if item['salary']:
                    salary_from = item['salary']['from']
                    salary_to = item['salary']['to']
                else:
                    salary_from = None
                    salary_to = None
                if item['address']:
                    city = item['address']['city']
                db_creator.fill_vacancies_table(cur,
                                                item['name'],
                                                item['employer']['name'],
                                                salary_from,
                                                salary_to,
                                                item['alternate_url'],
                                                city,

                                                )
    conn.close()


if __name__ == '__main__':
    main()
