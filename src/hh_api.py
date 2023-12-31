import requests


class HHApi:

    def __init__(self):
        self.url_vacancies = 'https://api.hh.ru/vacancies/'

    def get_emps_vacancies(self, employer_id):
        """Получает вакансии работодателей из файла"""
        result = []
        try:
            req = requests.get(self.url_vacancies,
                               params={'employer_id': str(employer_id), 'per_page': 100})
            if req.status_code == 200:
                data = req.json()
                pages = int(data['pages'])
                for page in range(pages):
                    req = requests.get(self.url_vacancies,
                                       params={'employer_id': str(employer_id), 'page': page, 'per_page': 100})
                    result.extend(req.json()['items'])
                    print(f'Страница {page+1} из {pages} загружена')
                print(f'Вакансии работодателя с id {employer_id} загружены!')
                return result
            else:
                return 'Ошибка подключения'
        except requests.exceptions.RequestException as error:
            print(error)
