from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, StaleElementReferenceException
from urllib3.exceptions import NewConnectionError, MaxRetryError
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import glob
import time

class AutobuyingAcc():

	def __init__(self, acc_number, articul, address):
		self.articul = articul
		self.address = address
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument("--disable-extensions")
		chrome_options.add_argument(f"user-data-dir=C:\\Users\\Георгий\\PycharmProjects\\Wildberries\\acc{acc_number}_completed")
		self.browser = webdriver.Chrome(options=chrome_options)
		self.browser.delete_all_cookies()

	def add_product_into_basket(self):
		self.browser.get(f'https://www.wildberries.ru/catalog/{self.articul}/detail.aspx?targetUrl=SP')
		time.sleep(2)
		self.browser.execute_script('window.scrollTo(0, 200)')
		try:
			self.browser.find_element_by_class_name("btn-main").click()
			time.sleep(2)
		except NoSuchElementException:
			print('Упал артикул, пробуем ещё раз')
			return 'wrong_articul'

	def attach_address(self):
		self.browser.get('https://www.wildberries.ru/lk/basket')
		time.sleep(2)
		self.browser.execute_script('window.scrollTo(0, 200)')
		address_items = self.address.replace(',', '').replace('Россия', '').split()

		try:
			# либо просто ставит новый адрес
			self.browser.find_element_by_css_selector("div.basket-delivery__choose-address").click()
			time.sleep(3)
			self.browser.find_element_by_class_name("popup__btn-main").click()
		except NoSuchElementException:
			# либо если уже заказывали хотя бы раз, то смотрит среди сохраненных адресов и меняет, если надо
			delivery = self.browser.find_element_by_css_selector("div.basket-delivery")
			delivery.find_element_by_css_selector("div.btn-change").click()
			time.sleep(3)
			saves = self.browser.find_elements_by_css_selector("li.history__item")
			# копается в сохранённых адресах
			for save in saves:
				success_address = True
				for u in address_items:
					if u.strip() in save.text:
						pass
					else:
						success_address = False
				if success_address:
					save.click()
					self.browser.implicitly_wait(1)
					self.browser.find_element_by_class_name("popup__btn-main").click()
					return
					# если нашёл нужную сохранку, то тыкает и выходит из функции
			# если же не нашёл, то тыкает на изменение адреса, и вводит новый
			self.browser.find_element_by_class_name("popup__btn-base").click()

		# вбивание адреса в карту
		WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.ymaps-2-1-79-searchbox-input__input')))
		input_address = self.browser.find_element_by_css_selector("input.ymaps-2-1-79-searchbox-input__input")
		input_address.send_keys(self.address)
		input_address.send_keys(Keys.ENTER)
		self.browser.implicitly_wait(3)
		# head = self.browser.find_element_by_class_name("popup__header")
		# head.click()
		# self.browser.implicitly_wait(3)
		btn_search_maps = self.browser.find_element_by_class_name("ymaps-2-1-79-searchbox-button")
		btn_search_maps.click()
		time.sleep(12)
		btn_search_maps.click()
		self.browser.implicitly_wait(1)
		# btn_list = self.browser.find_element_by_class_name("ymaps-2-1-79-searchbox-list-button")
		# btn_list.click()
		# self.browser.implicitly_wait(1)
		# btn_list.click()
		# self.browser.implicitly_wait(3)
		try:
			WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-islets__first')))
			# ac = ActionChains(self.browser)
			# ac.move_by_offset(920, 76).click().perform()
			self.browser.find_element_by_css_selector("ymaps.ymaps-2-1-79-islets__first").click()
			time.sleep(10)
		except NoSuchElementException:
			print('Не прогрузилась карта после поиска адреса, пробуем ещё раз')
			return 'map_error'

		# выбор слайда с адресом и подтверждение точки выдачи
		swiper_slides = self.browser.find_elements_by_css_selector("div.swiper-slide")
		# print(swiper_slides)
		for slide in swiper_slides:
			success_address = True
			for u in address_items:
				if u.strip() in slide.text:
					pass
				else:
					success_address = False
			if success_address:
				slide.click()
				break
			time.sleep(1)
		self.browser.find_element_by_css_selector("button.j-btn-select-poo").click()
		time.sleep(5)
		self.browser.find_element_by_class_name("popup__btn-main").click()
		time.sleep(5)

	def order_product(self):
		self.browser.execute_script('window.scrollTo(0, 400)')
		self.browser.find_element_by_class_name("b-btn-do-order").click()
		time.sleep(3)
		try:
			self.browser.find_element_by_css_selector("label.checkbox-with-text").click()
			self.browser.implicitly_wait(1)
			self.browser.find_element_by_class_name("popup__btn-main").click()
		except NoSuchElementException:
			pass

	def quit(self):
		self.browser.close()
		self.browser.quit()


if __name__=='__main__':
	list_of_addresses = [
		'Москва, Изумрудная 8',
		'Москва, Изумрудная 52',
		'Москва, Лётчика Бабушкина 41',
		'Москва, Тайнинская 16к1',
		'Москва, Минусинская 8',
		'Москва, Стартовая 33А',
		'Москва, Малыгина 1с2',
		'Москва, Анадырский проезд, 69',
		'Москва, Челюскинская 11',
		'Москва, Широкая 2',
		'Москва, Летчика Бабушкина 31',
		'Москва, Ленская 28',
		'Москва, проезд Шокальского, 61',
		'Москва, Широкая 13к4',
		'Москва, Студеный проезд, 14',
		'Москва, Заревый 9',
		'Москва, Лётчика Бабушкина 18',
		'Москва, Анадырский проезд, 13',
		'Москва, Широкая д.3 к3',
		'Москва, проезд Шокальского, 31к1',
	]

	# проверка артикула
	while True:
		articul = int(input('Артикул товара, который хотите выкупить: '))
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--headless')
		browser = webdriver.Chrome(options=chrome_options)
		browser.get(f'https://www.wildberries.ru/catalog/{articul}/detail.aspx?targetUrl=SP')
		try:
			button = browser.find_element_by_class_name("btn-main")
			browser.quit()
			break
		except NoSuchElementException:
			print('Товара, указанного Вами, не существует, попробуйте ещё раз\n')
			browser.quit()
	# проверка кол-ва акков
	# while True:
	# 	amount_accs = int(input('Количество выкупающих аккаунтов: '))
	# 	list_accs = glob.glob(r'.\acc*_completed')
	# 	if amount_accs > len(list_accs):
	# 		print(f'У Вас аккаунтов меньше, чем Вы ввели - {len(list_accs)}')
	# 	else:
	# 		break

	products_per_address = 4

	x = 7
	acc_number = int(input('Номер аккаунта, с которого начнется выкуп: '))

	while True:
			acc = AutobuyingAcc(acc_number, articul, list_of_addresses[(acc_number-1)//products_per_address])
			adding = acc.add_product_into_basket()
			if adding == 'wrong_articul':
				acc.quit()
				continue
			addressing = acc.attach_address()
			if addressing == 'map_error':
				acc.quit()
				continue
			acc.order_product()
			acc.quit()
			print(f'Аккаунт {acc_number} выкупил товар в {time.strftime("%H:%M:%S", time.gmtime())}')
			spat = round((7/(x-2))*3600)
			time.sleep(spat)
			x += spat/86400
			acc_number += 1
			if acc_number == 81:
				break

	print('Скрипт отработан!!!')


# https://www.wildberries.ru/lk/myorders/delivery
# find_element_by_class_name("delivery-code__value").text  это код, появляется сразу
# find_element_by_class_name("delivery-address__info").text  это адрес
# https://www.wildberries.ru/lk/details
# find_element_by_class_name("personal-data__header").text  это ФИО
