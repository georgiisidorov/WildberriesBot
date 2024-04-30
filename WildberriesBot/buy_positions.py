from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


def buy_position(acc_number, articul, address):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument(f"user-data-dir=C:\\Users\\Георгий\\PycharmProjects\\Wildberries\\acc{acc_number}_completed")
	browser = webdriver.Chrome(options=chrome_options)
	url = "https://www.wildberries.ru/"
	browser.get(url + f'catalog/{articul}/detail.aspx?targetUrl=SP')
	time.sleep(2)
	browser.execute_script('window.scrollTo(0, 200)')
	try:
		button = browser.find_element_by_class_name("btn-main")
		button.click()
	except NoSuchElementException:
		return 'Товара, указанного Вами, не существует, попробуйте ещё раз'
	time.sleep(2)
	browser.get(url + 'lk/basket')
	time.sleep(3)
	browser.execute_script('window.scrollTo(0, 200)')
	address = address.replace(',', '')
	address_items = address.split()
	try:
		choose_address = browser.find_element_by_css_selector("div.basket-delivery__choose-address")
		choose_address.click()
		time.sleep(2)
		btn_choose_address = browser.find_element_by_class_name("popup__btn-main")
		btn_choose_address.click()
		time.sleep(5)
	except NoSuchElementException:
		delivery = browser.find_element_by_css_selector("div.basket-delivery")
		btn_change = delivery.find_element_by_css_selector("div.btn-change")
		btn_change.click()
		time.sleep(2)
		saves = browser.find_elements_by_css_selector("li.history__item")
		for save in saves:
			success_address = True
			text = slide.text
			for u in address_items:
				if u.strip() != 'Россия':
					if u.strip() in text:
						pass
					else:
						success_address = False
			if success_address:
				slide.click()
				return
		btn_change_address = browser.find_element_by_class_name("popup__btn-base")
		btn_change_address.click()
		time.sleep(5)
	search_maps = browser.find_element_by_css_selector("input.ymaps-2-1-79-searchbox-input__input")
	search_maps.send_keys(address)
	time.sleep(1)
	btn_search_maps = browser.find_element_by_class_name("ymaps-2-1-79-searchbox-button")
	btn_search_maps.click()
	time.sleep(1)
	btn_search_maps.click()
	time.sleep(3)
	try:
		btnitem_search_maps = browser.find_element_by_css_selector("ymaps.ymaps-2-1-79-islets__first")
		btnitem_search_maps.click()
		time.sleep(2)
	except:
		return 'Не прогрузилась карта после поиска адреса'
	swiper_slides = browser.find_elements_by_css_selector("div.address-item")
	for slide in swiper_slides:
		success_address = True
		text = slide.text
		for u in address_items:
			if u.strip() != 'Россия':
				if u.strip() in text:
					pass
				else:
					success_address = False
		if success_address:
			slide.click()
	time.sleep(3)
	btn_select = browser.find_element_by_css_selector("button.j-btn-select-poo")
	btn_select.click()
	time.sleep(2)
	btn_choose_address = browser.find_element_by_class_name("popup__btn-main")
	btn_choose_address.click()

# работает, но неидеально, он должен во вторые и дальше заказы учитывать сохраненный адрес 
# и вбивать новый, если надо
# 74, 75 и 76 акки

acc_number = int(input('Номер аккаунта, который хотите открыть: '))
articul = int(input('Артикул товара, который хотите выкупить: '))
buy_position(acc_number, articul, 'Россия, Москва, Летчика Бабушкина 31')
