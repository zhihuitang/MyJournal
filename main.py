import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def find_elements_by_xpath(driver, path, timeout):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, path)))


TIMEOUT = 30


def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("python main.py [personal-id] [download-excel: 0/1]")
        sys.exit(0)

    personal_id = sys.argv[1]
    download_excel = sys.argv[2]

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    prefs = {
      "translate_whitelists": {"fr":"en"},
      "translate":{"enabled":"true"}
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # driver = webdriver.Firefox()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.1177.se/Stockholm/")

    assert "1177" in driver.title
    button = driver.find_elements_by_xpath("//*[contains(text(), 'Logga in')]")[0]
    button.click()

    next_button = find_elements_by_xpath(driver, "//a[text()='Logga in med e-legitimation']", TIMEOUT)
    next_button.click()

    mobile_bankid_button = find_elements_by_xpath(driver, "//a[text()='Mobilt BankID']", TIMEOUT)
    mobile_bankid_button.click()

    # input_text = driver.find_element_by_xpath("//input[id='mbidentifier']")
    input_text = driver.find_element_by_name("mbiidentifier")
    input_text.send_keys(personal_id)

    submit_button = driver.find_element_by_xpath("//input[@type='submit']")
    submit_button.click()

    # <a href="/mvk/services.xhtml?tab=1#tabs-1" class="itemNavigation assistiveText">Gå till Journal</a>
    #journal_arrow = find_elements_by_xpath("//a[@class='itemNavigation assistiveText' and text()='Gå till Journal']", 120)
    journal_arrow = find_elements_by_xpath(driver, "//h4[text()='Journaltjänster']", 180)
    journal_arrow.click()

    # <a href="https://journalen.1177.se?hsaid=SE162321000024-1177&amp;dynamicid=KONT-9DZFUX" class="itemNavigation assistiveText">Gå till tjänsten Journalen</a>
    journalen_arrow = find_elements_by_xpath(driver, "//a[@class='itemNavigation assistiveText' and text()='Gå till tjänsten Journalen']", TIMEOUT)
    journalen_arrow.click()

    view_all_button = find_elements_by_xpath(driver, "//button[@id='btnShowRespite' and text()='Visa alla uppgifter']", TIMEOUT)
    view_all_button.click()

    provsvar = find_elements_by_xpath(driver, "//div[@class='journal-category-item' and @data-configurable-module=8]", TIMEOUT)
    provsvar.click()

    if download_excel == "1":
        export_to_excel = find_elements_by_xpath(driver, "//a[@id='export-to-excel']", TIMEOUT)
        export_to_excel.click()

    # driver.close()


if __name__ == "__main__":
    main()

