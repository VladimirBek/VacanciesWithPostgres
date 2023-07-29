from fill_tables import fill_tables
from src.db_manager import DBManager


def main():
    db_manger = DBManager()
    conn = db_manger.start_connection()
    conn.autocommit = True
    while True:
        user_input = input('Выберете функцию\n'
                           '1 - получить список всех компаний и количество вакансий у каждой компании\n'
                           '2 - получить список всех вакансий с указанием названия компании, '
                           'названия вакансии и зарплаты и ссылки на вакансию\n'
                           '3 - получить среднюю зарплату по вакансиям\n'
                           '4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
                           '5 - получить список всех вакансий, в названии которых содержатся переданные в метод слова, '
                           'например “python”\n'
                           '0 - выйти из программы\n'
                           'Ваш выбор: ')
        print()
        if user_input == '1':
            with conn.cursor() as cur:
                for row in db_manger.get_companies_and_vacancies_count(cur):
                    print(f'Компания {row[0]} (количество вакансий - {row[1]})')
                    print()
        elif user_input == '2':
            with conn.cursor() as cur:
                for row in db_manger.get_all_vacancies(cur):
                    name, employer, salary_from, salary_to, url = row
                    if salary_to and salary_from:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата от {salary_from} до {salary_to} руб.\n'
                              f'Ссылка на вакансию {url}')

                    elif salary_from and not salary_to:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата от {salary_from} руб.\n'
                              f'Ссылка на вакансию {url}')
                        print()
                    elif not salary_from and salary_to:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата до {salary_to} руб.\n'
                              f'Ссылка на вакансию {url}')
                        print()
                    else:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата не указана\n'
                              f'Ссылка на вакансию {url}')
                        print()
        elif user_input == '3':
            with conn.cursor() as cur:
                print(int(db_manger.get_avg_salary(cur)[0][0]), 'рублей - средняя зарплата по всем вакансиям')

        elif user_input == '4':
            with conn.cursor() as cur:
                avg = db_manger.get_avg_salary(cur)[0][0]
                for row in db_manger.get_vacancies_with_higher_salary(cur, avg):
                    name, employer, salary_from, salary_to, url = row[1:6]
                    if salary_to and salary_from:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата от {salary_from} до {salary_to} руб.\n'
                              f'Ссылка на вакансию {url}\n')

                    elif salary_from and not salary_to:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата от {salary_from} руб.\n'
                              f'Ссылка на вакансию {url}\n')
                        print()
                    elif not salary_from and salary_to:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата до {salary_to} руб.\n'
                              f'Ссылка на вакансию {url}\n')
                        print()
                    else:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата не указана\n'
                              f'Ссылка на вакансию {url}\n')
                        print()
        elif user_input == '5':
            with conn.cursor() as cur:
                user_word = input('Введите ключевое слово: ')
                for row in db_manger.get_vacancies_with_keyword(cur, user_word):
                    name, employer, salary_from, salary_to, url = row[1:6]
                    if salary_to and salary_from:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата от {salary_from} до {salary_to} руб.\n'
                              f'Ссылка на вакансию {url}\n')

                    elif salary_from and not salary_to:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата от {salary_from} руб.\n'
                              f'Ссылка на вакансию {url}\n')
                        print()
                    elif not salary_from and salary_to:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата до {salary_to} руб.\n'
                              f'Ссылка на вакансию {url}\n')
                        print()
                    else:
                        print(f'Вакансия: {name}\n'
                              f'Компания: {employer}\n'
                              f'Зарплата не указана\n'
                              f'Ссылка на вакансию {url}\n')
                        print()
        elif user_input == '0':
            return
        else:
            print('Введена неверная команда, попробуйте заново')


if __name__ == '__main__':
    fill_tables()
    main()
