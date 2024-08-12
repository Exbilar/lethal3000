import pyperclip
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

if os.getcwd().endswith("lethal3000"):
    os.chdir(os.getcwd() + "/dataset")

print(os.getcwd())

addr_list = []

for page in range(1):
    driver.get("https://etherscan.io/contractsVerified/" + (str(page + 1) if page > 0 else ""))
    for row in range(25):
        retry = True
        try:
            while (retry):
                row_selector = '//tbody[contains(@class, "text-nowrap")]/tr[{}]'.format(row + 1)
                address_selector = row_selector + '/td[1]/span[1]/a/span/span'
                select_item = driver.find_element(by=By.XPATH, value=address_selector)
                addr = select_item.get_attribute("data-highlight-target")
                addr_list.append(addr)
                print(addr)
                retry = False
        finally:
            retry = True
    sleep(10)

with open("./contract_address.txt", "w") as file:
    for addr in addr_list:
        file.writelines(addr + "\n")

for addr in addr_list:
    driver.get("https://etherscan.io/address/" + str(addr) + "#code")
    os.makedirs("./" + str(addr), exist_ok=True)

    # contract_name = driver.find_element(by=By.XPATH, value='//*[@id="ContentPlaceHolder1_contractCodeDiv"]/div[2]/div[1]/div[1]/div[2]/span')
    # contract_name = contract_name.get_attribute('innerHTML')

    # compiler_version = driver.find_element(by=By.XPATH, value='//*[@id="ContentPlaceHolder1_contractCodeDiv"]/div[2]/div[1]/div[2]/div[2]/span')
    # compiler_version = compiler_version.get_attribute('innerHTML')

    # description = f'["contract name": "{contract_name}", "compiler version": "{compiler_version}"]'
    # with open("./" + str(addr) + "/description.json", "w") as f:
    #     f.write(description)

    # copy contract ABI to clipboard

    copy_btn = driver.find_element(by=By.XPATH, value='//a[@aria-label="Copy ABI to clipboard"]')
    driver.execute_script("arguments[0].click()", copy_btn)
    sleep(1)

    abi = pyperclip.paste()
    print(abi)

    with open("./" + str(addr) + "/abi.json", "w") as f:
        f.write(abi)

    # headers = driver.find_elements(by=By.XPATH, value='//div[@id="dividcode"]/div//h4')
    # num = 1
    # for header in headers:
    #     if "Deployed Bytecode" in str(header.get_attribute("innerHTML")):
    #         break
    #     num += 1

    # bytecode_box = driver.find_element(by=By.XPATH, value='//div[@id="dividcode"]/div[{}]/pre'.format(num))
    # bytecode = bytecode_box.get_attribute("innerHTML")
    # print(bytecode)

    # with open("./" + str(addr) + "/bytecode.bin", "w") as f:
    #     f.write(bytecode)

    # source_codes = driver.find_elements(by=By.XPATH, value='//a[@aria-label="Copy source code to clipboard"]')
    # num = 0
    # for code in source_codes:
    #     driver.execute_script("arguments[0].click()", code)
    #     sleep(2)
    #     res = pyperclip.paste()
    #     print(res)
    #     with open("./" + str(addr) + f"/code{num}.sol", "w") as f:
    #         f.write(res)
    #     num += 1
    # sleep(10)

driver.quit()