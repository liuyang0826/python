from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from time import sleep
from configparser import ConfigParser
from os import getcwd, path

# 读取配置
config = ConfigParser()
cwd  = getcwd()
file = path.join(cwd, 'conf.ini')
config.read(file, encoding="utf-8")
username = config.get("defaults", "username")
password = config.get("defaults", "password")
project_type = config.get("defaults", "project_type")
project_code = config.get("defaults", "project_code")
project_hour = config.get("defaults", "project_hour")
project_remark = config.get("defaults", "project_remark")
auto_submit = config.getboolean("defaults", "auto_submit")
submit_remark = config.get("defaults", "submit_remark")

# 初始化webdriver
options = webdriver.EdgeOptions()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Edge(service=Service("./msedgedriver.exe"), options=options)
driver.get('http://122.9.144.53/seeyon/main.do?method=main')

# 登录
driver.find_element(by=By.CSS_SELECTOR, value="#login_username").send_keys(username)
driver.find_element(by=By.CSS_SELECTOR, value="#login_password").send_keys(password)
driver.find_element(by=By.CSS_SELECTOR, value="#login_button").click()
sleep(2)
# 跳转工时表单
driver.find_element(by=By.CSS_SELECTOR, value="table > tbody > tr:nth-child(1) > td.col_first > div > a").click()
driver.switch_to.window(driver.window_handles[1])
driver.implicitly_wait(30)
driver.switch_to.frame("zwIframe")
# 项目类型按钮
driver.find_element(by=By.CSS_SELECTOR, value=".cap-icon-mingxibiaoxuanzeqi").click()
# 项目类型列表
driver.find_element(by=By.CSS_SELECTOR, value="#mineFormPage > section > li:nth-child(" + project_type + ")").click()
driver.switch_to.parent_frame()
driver.switch_to.frame(driver.find_element(by=By.CSS_SELECTOR, value="#RelationPage_main > iframe"))
# 过滤选择项目
driver.find_element(by=By.CSS_SELECTOR, value="input[type='text']").send_keys(project_code)
driver.find_element(by=By.CSS_SELECTOR, value="button.cap4-condition-button.cap4-condition-button__filter").click()
sleep(2)
driver.find_element(by=By.CSS_SELECTOR, value="input[type='checkbox']").click()
driver.switch_to.parent_frame()
driver.find_element(by=By.CSS_SELECTOR, value="a[id^='layui-layer-btn']").click()
driver.switch_to.frame("zwIframe")
# 输入工时
driver.find_element(by=By.CSS_SELECTOR, value="div[id^='field'] div:nth-child(2) > input").send_keys(project_hour)
driver.find_element(by=By.CSS_SELECTOR, value="section[id^='tableName-front_formson'] div.cap4-text__cnt input").send_keys(project_remark)
driver.switch_to.parent_frame()
driver.find_element(by=By.CSS_SELECTOR, value="#content_deal_comment").send_keys(submit_remark)
# 提交
if auto_submit:
  driver.find_element(by=By.CSS_SELECTOR, value="#_dealSubmit").click()
  driver.quit()
  exit(0)
