from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import load_workbook
import re

tb = 'example.xlsx'
wb = load_workbook(tb)
ws = wb['Sheet1']


#cities: Калининград, Москва, Новосибирск, Хабаровск

# 1)разбить на функции(change_city(name), get_price(id))

# Замените на путь к файлу драйвера
# driver_path = "C:/Users/adska/OneDrive/Рабочий стол/chromedriver.exe"
# driver = webdriver.Chrome(executable_path=driver_path)

# Открываем страницу Google
# driver.get("https://www.ozon.ru/product/kofe-rastvorimyy-egoiste-noir-100-g-34362278/")

# # Находим поле для ввода поискового запроса и вводим текст
# login_box = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
# password_box = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
# login_box.send_keys("adskayagonchaya6")
# login_box.send_keys(Keys.RETURN)
# time.sleep(10)

# def main():
#     for i in range(0, len(links)):
#         driver_path = "C:/Users/adska/OneDrive/Рабочий стол/chromedriver.exe"
#         driver = webdriver.Chrome(executable_path=driver_path)
#         driver.get(links[i])
#         city_box = driver.find_elements(By.CLASS_NAME, 'x5-a1')[1]
#         price_box = driver.find_element(By.CLASS_NAME, 'nq1')
#         article_box = driver.find_element(By.CLASS_NAME, 'sm6')
#         city_box.click()
#         time.sleep(10)
#         driver.implicitly_wait(5)
#         driver.quit()


def get_price(link):
    driver_path = "C:/Users/adska/OneDrive/Рабочий стол/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(link)
    age_box = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    age_box.send_keys("01012000")
    age_box.send_keys(Keys.RETURN)
    time.sleep(5)
    # confirm_box = driver.find_element(By.CSS_SELECTOR, '[type="button"]')
    # confirm_box.click()
    time.sleep(5)
    price_box = driver.find_element(By.CLASS_NAME, 'qn1')
    price = price_box.text.strip()[:-1]
    price = re.findall(r'\d+', price)
    price1 = ''
    for i in range(0, len(price)):
        price1 += price[i]
    return int(price1)




# print(login_box.text.split("₽")[0].strip())

if __name__ == '__main__':
    link = 'https://www.ozon.ru/product/vibrator-krolik-dlya-devushek-i-zhenshchin-9-rezhimov-klitoralnyy-stimulyator-seks-igrushki-tovary-657401063/?advert=7P_hOuYeqfiw49AMoThMlndmNYPorayypCyQxZE6JD4XL2SZfypD4D6EHpElDmi4pHCqIVFkXnMZs2W0lEoruBcrUjoz2-JI92z2MS2QB67O6JeBcuqHQPv_ddRxDoY3SbC8hXGbwapWkcJDKlgqhIKp68HWv4ryL8KapIZ_Fm5Kp0aV_mJ1cPkpIUEDifWVgjT_iHI8huqQEHAO-EAUDM8-qDUL0pUZ4Qk5gu0owyUBShF1T_IyCF_u1TsbvbrKdnR6lWeOC-r93jG3aawGurTfBUo2-Q&avtc=1&avte=2&avts=1681139560&keywords=657401063&sh=rNoJ3tbTUw'
    get_price(link)




# # Даем время загрузиться результатам поиска
# driver.implicitly_wait(5)

# Закрываем драйвер
wb.save(tb)
wb.close()
# driver.quit()