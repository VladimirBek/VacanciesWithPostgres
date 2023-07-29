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
        employer_id = 0
        for employer in ids:
            employer_id += 1
            items = hh.get_emps_vacancies(employer)
            if items[0]['area']:
                city = items[0]['area']['name']
            else:
                city = None
            employer_name = items[0]['employer']['name']
            db_creator.fill_employers_table(cur, employer_name,
                                            items[0]['employer']['alternate_url'],
                                            city,
                                            len(items))
            for item in items:

                if item['salary']:
                    salary_from = item['salary']['from']
                    salary_to = item['salary']['to']
                else:
                    salary_from = None
                    salary_to = None
                if item['address']:
                    city = item['area']['name']
                else:
                    city = None

                db_creator.fill_vacancies_table(cur,
                                                item['name'],
                                                item['employer']['name'],
                                                salary_from,
                                                salary_to,
                                                item['alternate_url'],
                                                city, employer_id)
    conn.close()


if __name__ == '__main__':
    main()
