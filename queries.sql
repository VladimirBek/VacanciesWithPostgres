-- запросы для работы с таблицами (используются в классе db_manager)
SELECT employer_name, vacancies_count FROM employers;
SELECT vacancy_name, employer_name, salary_from, salary_to, url FROM vacancies;
SELECT AVG(salary_from + salary_to) AS avg_salary FROM vacancies;
SELECT * FROM vacancies WHERE (salary_from + salary_to)/2 > 141446 GROUP BY vacancy_id;
SELECT * FROM vacancies WHERE vacancy_name LIKE '%Грузчик%' OR vacancy_name LIKE '%грузчик%';
