from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import xlsxwriter

def collect_information(number):
	file_spisok = []

	for acc in range(1, number+1):
		print(acc)
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument(f"user-data-dir=C:\\Users\\Георгий\\PycharmProjects\\Wildberries\\acc{acc}_completed")
		chrome_options.add_argument('--headless')
		chrome_options.add_argument("--disable-extensions")
		browser = webdriver.Chrome(options=chrome_options)
		browser.get('https://www.wildberries.ru/lk/myorders/delivery')
		WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'delivery-code__value')))
		code = browser.find_element_by_class_name("delivery-code__value").text
		address = browser.find_element_by_class_name("delivery-address__info").text
		browser.get('https://www.wildberries.ru/lk/details')
		WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'personal-data__header')))
		phone = browser.find_element_by_css_selector("li.personal-data__item--phone").text.replace('Телефон\n', '').replace(' ', '')
		fi = browser.find_element_by_class_name("personal-data__header").text
		file_spisok.append((address, code, fi, phone))
		browser.quit()

	workbook = xlsxwriter.Workbook('collected_info.xlsx')
	worksheet_info = workbook.add_worksheet()
	bold = workbook.add_format({'bold': True})
	worksheet_info.write('A1', 'Адрес', bold)
	worksheet_info.write('B1', 'Код', bold)
	worksheet_info.write('C1', 'Имя', bold)
	worksheet_info.write('D1', 'Телефон', bold)

	for i, (address, code, fi, phone) in enumerate(file_spisok, start=2):
		worksheet_info.write(f'A{i}', address)
		worksheet_info.write(f'B{i}', code)
		worksheet_info.write(f'C{i}', fi)
		worksheet_info.write(f'D{i}', phone)

	worksheet_info.set_column('A:A', 50)
	worksheet_info.set_column('C:C', 25)
	worksheet_info.set_column('D:D', 15)
	workbook.close()

number = int(input('Кол-во выкупивших аккаунтов: '))
collect_information(number)



