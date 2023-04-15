from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import load_workbook
import re
from selenium.webdriver.firefox.options import Options
import json
import undetected_chromedriver.v2 as uc
from selenium.webdriver.chrome.service import Service
import zipfile

tb = 'example.xlsx'
wb = load_workbook(tb)
ws = wb['Sheet1']
#
# firefox_options = Options()
# firefox_options.set_preference("dom.webdriver.enabled", False)
#
# options = Options()
# options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# driver = webdriver.Firefox(executable_path=r'geckodriver.exe', options=options)

# driver = webdriver.Firefox(executable_path=driver_path, options=firefox_options)

#cities: Калининград, Москва, Новосибирск, Хабаровск

# 1)разбить на функции(change_city(name), get_price(id))

# Замените на путь к файлу драйвера
driver_path = "chromedriver.exe"
# opts = Options()
# opts.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
driver = webdriver.Chrome(executable_path=driver_path)
# driver.execute_cdp_cmd('Network.setUserAgentOverride', {"sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"'})

PROXY_HOST = '185.66.15.75'
PROXY_PORT = 9739  # Your proxy port
PROXY_USER = 'Xn0Y5x'
PROXY_PASS = 'hahtyA'

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"76.0.0"
}
"""

background_js = """
let config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)



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

def get_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()

    if use_proxy:
        plugin_file = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr('manifest.json', manifest_json)
            zp.writestr('background.js', background_js)

        chrome_options.add_extension(plugin_file)

    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')

    s = Service(
        executable_path='chromedriver.exe'
    )
    driver = webdriver.Chrome(
        service=s,
        options=chrome_options
    )

    return driver


def get_price(link):
    # driver = get_chromedriver(use_proxy=True,
    #                          user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #           const newProto = navigator.__proto__
    #           delete newProto.webdriver
    #           navigator.__proto__ = newProto
    #           """
    # })
    # load_cookies()
    driver.get(link)
    # driver.refresh()
    age_box = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    age_box.send_keys("01012000")
    age_box.send_keys(Keys.RETURN)
    time.sleep(5)
    confirm_box = driver.find_element(By.CSS_SELECTOR, '[type="button"]')
    confirm_box.click()
    time.sleep(5)
    price_box = driver.find_element(By.CLASS_NAME, 'qn1')
    price = price_box.text.strip()[:-1]
    price = re.findall(r'\d+', price)
    price1 = ''
    for i in range(0, len(price)):
        price1 += price[i]
    driver.close()
    return int(price1)


def load_cookies():
    driver = uc.Chrome()
    cookies_path = 'cookies.json'
    with open(cookies_path, 'r') as file:
        src = json.load(file)


    # for cookie1 in src:
    #     for key, value in cookie1.items():
    #         # driver.add_cookie(cookie2)
    #         driver.add_cookie({'name': key, 'value': value})

    for cookie in src:
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'

        if not cookie["sameSite"] in ["Strict", "Lax", "None"]:
            cookie['sameSite'] = 'Strict'

        driver.add_cookie(cookie)



if __name__ == '__main__':
    link = 'https://www.ozon.ru/product/vibrator-krolik-dlya-devushek-i-zhenshchin-9-rezhimov-klitoralnyy-stimulyator-seks-igrushki-tovary-657401063/?advert=7P_hOuYeqfiw49AMoThMlndmNYPorayypCyQxZE6JD4XL2SZfypD4D6EHpElDmi4pHCqIVFkXnMZs2W0lEoruBcrUjoz2-JI92z2MS2QB67O6JeBcuqHQPv_ddRxDoY3SbC8hXGbwapWkcJDKlgqhIKp68HWv4ryL8KapIZ_Fm5Kp0aV_mJ1cPkpIUEDifWVgjT_iHI8huqQEHAO-EAUDM8-qDUL0pUZ4Qk5gu0owyUBShF1T_IyCF_u1TsbvbrKdnR6lWeOC-r93jG3aawGurTfBUo2-Q&avtc=1&avte=2&avts=1681139560&keywords=657401063&sh=rNoJ3tbTUw'
    get_price(link)




# # Даем время загрузиться результатам поиска
# driver.implicitly_wait(5)

# Закрываем драйвер
wb.save(tb)
wb.close()
# driver.quit()