from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import emoji

# from webdriver_manager.chrome import ChromeDriverManager
from file_read_write import *

chromed_driver = 'chromedriver'


class WhatsApp:

    def __init__(self):
        self.all_data = read_contacts_data()
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(chromed_driver)        
        self.driver.get("https://web.whatsapp.com")
        print("Scan QR Code, And then Enter")
        # input()
        print("Logged In")

    def send_message(self, contact, text):
        try:
            self.search_item(contact)
            inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
            input_box = self.driver.find_element_by_xpath(inp_xpath)
            # time.sleep(2)
            # input_box.send_keys(text + Keys.ENTER)

            for line in text.split('\n'):
                ActionChains(self.driver).send_keys(emoji.emojize(line)).perform()
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(
                    Keys.ENTER).perform()
            ActionChains(self.driver).send_keys(Keys.RETURN).perform()

        except:
            print("----contact not found----", contact)

    def send_image(self, msg, img_path, contact):
        try:
            self.search_item(contact)
            attachment_box = self.driver.find_element_by_xpath('//div[@title = "Attach"]')
            attachment_box.click()
            image_box = self.driver.find_element_by_xpath(
                '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            image_box.send_keys(img_path)
            time.sleep(2)
            text_message = self.driver.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]')
            time.sleep(1)

            for line in msg.split('\n'):
                ActionChains(self.driver).send_keys(line).perform()
                ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(
                    Keys.ENTER).perform()
            ActionChains(self.driver).send_keys(Keys.RETURN).perform()


            # text_message.send_keys(msg)
         #   send_button = self.driver.find_element_by_xpath("//div[@class='_3y5oW _3qMYG']")
          #  send_button.click()
        except:
            print("----contact not found----", contact)

    def send_file(self,filepath, contact):
        try:
            self.search_item(contact)
            attachment_box = self.driver.find_element_by_xpath('//div[@title = "Attach"]')
            attachment_box.click()
            image_box = self.driver.find_element_by_xpath(
                '//input[@accept="*"]')
            image_box.send_keys(filepath)
            time.sleep(3)
            send_button = self.driver.find_element_by_xpath("//div[@class='_3y5oW _3qMYG']")
            send_button.click()
            attachment_box.click()
            time.sleep(1)
        except:
            print("----contact not found----", contact)

    def search_item(self,contact):
        self.search_box = self.driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
        self.search_box.clear()
        self.search_box.send_keys(contact)
        time.sleep(2)
        selected_contact = self.driver.find_element_by_xpath("//span[@title='" + contact + "']")
        selected_contact.click()

    def send_message_to_list(self, val, msg, image_path=None, file_path=None, start=0, end=0):
            
        receivers = self.all_data[val]
        receivers = self.get_splited_list(start, end, receivers)
        total_receivers = len(receivers)
        print("start_", start)
        print("end_", end)
        print(total_receivers)
        index = 1
        for c in receivers:
            if image_path:
                self.send_image(msg, image_path, c)
            elif file_path:
                self.send_file(file_path, c)
            else:
                self.send_message(c, msg)
            print("sending ....msg... "+str(index) + "/"+str(total_receivers))
            index += 1
            time.sleep(4)

        time.sleep(10)
        # self.driver.close()
        print("your task has been completed !")
        return True

    def get_splited_list(self, start_index, end_index, data):
        if start_index > end_index:
            start_index, end_index = end_index, start_index
        return data[start_index:end_index + 1]


time.sleep(10)
# driver.quit()
