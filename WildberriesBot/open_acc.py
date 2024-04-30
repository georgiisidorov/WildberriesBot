from selenium import webdriver
from urllib3.exceptions import NewConnectionError, MaxRetryError
from selenium.common.exceptions import WebDriverException

def open_acc(acc_number):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument(f"user-data-dir=C:\\Users\\Георгий\\PycharmProjects\\Wildberries\\acc{acc_number}_completed")
	chrome_options.add_argument("--disable-extensions")
	browser = webdriver.Chrome(options=chrome_options)
	url = "https://www.wildberries.ru/lk/details"
	browser.get(url)


acc_number = int(input('Номер аккаунта: '))
try:
	open_acc(acc_number)
except ConnectionRefusedError:
	pass
except NewConnectionError:
	pass
except MaxRetryError:
	pass
except WebDriverException:
	pass
