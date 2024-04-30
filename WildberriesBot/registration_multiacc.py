from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import json
from python3_anticaptcha import ImageToTextTask
import requests
import os
import glob
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from python3_anticaptcha.errors import ReadError
from urllib3.exceptions import NewConnectionError, MaxRetryError
from requests.exceptions import ConnectionError

api_keys = [
'257AAd7f3d27635255c80e641c972698',
'f279A30ce1d1deAbdA4687758df2d06c',
'0bc48dA6cd482e8d518e4f6396e08266',
'16ded4e96966f3c683d08fc6264cf605',
'd3cb1291c6901b7d7430397b773cfcAc',
'1471e6ccf2889feA479028901b6dc165',
'Be1d22236fBd0fc8639872cBc40ece95',
'f6b0A90102A756dc2006Ae70dA5A76ff',
'e658e42A90ed041692bA8b9cdf96A90A',
'B3c385ef65B883f012f0e66dfB156558'
]
api_key_1 = '257AAd7f3d27635255c80e641c972698'
api_key_2 = 'f279A30ce1d1deAbdA4687758df2d06c'
api_key_3 = '0bc48dA6cd482e8d518e4f6396e08266'
url = 'https://sms-activate.ru/stubs/handler_api.php?'


def getBalance(api_key):
	params = urlencode({'api_key': api_key, 'action': 'getBalance'})
	URL = url + params
	response = requests.get(URL)
	return response.text


def getNumber(api_key):
	params = urlencode({'api_key': api_key, 'action': 'getNumber', 'service': 'uu', 'country': '0'})
	URL = url + params
	response = requests.get(URL)
	return response.text


def setStatus(api_key, id, status):
	params = urlencode({'api_key': api_key, 'action': 'setStatus', 'status': str(status), 'id': id})
	URL = url + params
	response = requests.get(URL)
	return response.text


def getStatus(api_key, id):
	params = urlencode({'api_key': api_key, 'action': 'getStatus', 'id': id})
	URL = url + params
	response = requests.get(URL)
	return response.text


def WB_number(api_key, id, number, acc_number):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument(f"user-data-dir=C:\\Users\\Георгий\\PycharmProjects\\Wildberries\\acc{acc_number}")
	# chrome_options.add_extension("C:\\Users\\Георгий\\PycharmProjects\\Wildberries\\Proxy\\residentproxy2.zip")
	# chrome_options.add_argument("--disable-extensions")
	browser = webdriver.Chrome(options=chrome_options)
	url = "https://www.wildberries.ru/security/login"
	browser.get(url)
	time.sleep(1)
	number_broken = False
	captcha_broken = False
	try:
		elem1 = browser.find_element_by_class_name("input-item")
		elem1.send_keys(str(number)[1:])
		time.sleep(1)
		button = browser.find_element_by_id("requestCode")
		button.click()
		time.sleep(2)
	except NoSuchElementException:
		number_broken = True
	while True and not number_broken:
		try:
			button_reload = browser.find_element_by_class_name("captcha-reload")
		except NoSuchElementException:
			captcha_broken = True
			break
		try:
			image_link = browser.find_element_by_class_name("captcha-image").get_attribute('src').split('base64,')[1]
		except NoSuchElementException:
			button_reload.click()
			time.sleep(2)
			continue
		try:
			antcpt = ImageToTextTask.ImageToTextTask(anticaptcha_key = '5ded9985ca92c0d82c49ec3005537c33').captcha_handler(captcha_base64=image_link)
		except Exception:
			button_reload.click()
			time.sleep(2)
			continue
		try:
			captcha_answer = antcpt['solution']['text']
		except KeyError:
			print(antcpt)
			captcha_broken = True
			break
		captcha_text = browser.find_element_by_id("smsCaptchaCode")
		captcha_text.send_keys(captcha_answer)
		button_captcha = browser.find_element_by_class_name("btn-submit")
		button_captcha.click()
		time.sleep(2)
		try:
			element = browser.find_element_by_class_name("field-validation-error")
			if element.text == '':
				break
		except NoSuchElementException:
			break
	time.sleep(2)
	if number_broken:
		print("Сломался ввод телефона")
		setStatus(api_key, id, 8)
		browser.close()
		browser.quit()
		time.sleep(3)
	if captcha_broken:
		print("Сломалась капча")
		setStatus(api_key, id, 8)
		browser.close()
		browser.quit()
		time.sleep(3)
	else:
		text = browser.find_element_by_class_name("login-block-text").text
		if 'поступит звонок' in text:
			wb = False
		if "выслан" in text:
			wb = True
		if text == '':
			wb == False
		if wb:
			print('СМС УРААААА')
			setStatus(api_key, id, 1)
			code = ''
			for i in range(3):
				time.sleep(30)
				status = getStatus(api_key, id)
				if 'STATUS_OK' in status:
					code = status.split(':')[1]
					break
				time.sleep(30)
			if code == '':
				setStatus(api_key, id, 8)
				browser.close()
				browser.quit()
				time.sleep(3)
				# button.click()
				# setStatus(id, 3)
				# for i in range(3):
				# 	time.sleep(30)
				# 	status = getStatus(id)
				# 	if 'STATUS_OK' in status:
				# 		code = status.split(':')[1]
				# 	time.sleep(30)
			if code != '':
				code_area = browser.find_element_by_class_name("symbols-4")
				code_area.send_keys(code)
				time.sleep(2)
				setStatus(api_key, id, 6)
				browser.close()
				browser.quit()
				time.sleep(3)
				os.rename(f'.\\acc{acc_number}', f'.\\acc{acc_number}_completed')
				acc_number += 1
				return acc_number
			# if code == '':
			# 	setStatus(id, 8)
			# 	browser.close()
			# 	os.system('taskkill /f /im chromedriver.exe')
			# 	time.sleep(30)
		else:
			current_time = time.strftime("%H:%M:%S", time.gmtime())
			print(f'звонок {current_time}')
			setStatus(api_key, id, 8)
			browser.close()
			browser.quit()
			time.sleep(3)



def main(amount):
	acc_number = len(glob.glob(r'.\acc*_completed')) + 1
	number_fallen = 0
	counter_fallen = 0
	api_key_i = 0
	finish_number = acc_number + amount
	while acc_number != finish_number:
		try:
			text = getNumber(api_keys[api_key_i])
			if 'ACCESS_NUMBER' in text:
				response_list = text.split(':')
				id, number = response_list[1], response_list[2]
				wbc = WB_number(api_keys[api_key_i], id, number, acc_number)
				if wbc is None:
					counter_fallen += 1
				else:
					acc_number = wbc
					counter_fallen = 0
			if 'NO_BALANCE' in text:
				counter_fallen = 2
			if 'BANNED' in text:
				counter_fallen = 2
			if counter_fallen == 2:
				counter_fallen = 0
				number_fallen += 2
				if number_fallen != 2*len(api_keys):
					api_key_i += 1
				else:
					api_key_i = 0
		except IndexError:
			api_key_i = 0
		except TimeoutError:
			pass
		except NewConnectionError:
			pass
		except MaxRetryError:
			pass
		except ConnectionError:
			pass
		except WebDriverException:
			pass



amount = int(input('Кол-во аккаунтов, которое нужно зарегистрировать: '))
for i in range(len(api_keys)):
	print(f'Баланс {i+1}го SmsActivate акка: ' + getBalance(api_keys[i]).split(':')[1] + '₽')

main(amount)

# errorId 2
