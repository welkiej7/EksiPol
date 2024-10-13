from selenium import webdriver
from time import sleep, time
import json
from selenium.webdriver.common.by import By

'''
Title: EksiSozluk User Data Scraper
Author: Onur Tuncay Bal
Date: 2024 - Summer
Last Update: 2024 - Summer

'''


class MorPan:
    def __init__(self) -> None:

        with open('user_credentials.json') as file:
            self.CREDENTIALS = json.load(file)
        file.close()
        self.logged_in = False
        self.USER_URL = "https://eksisozluk.com/biri/"
        self.FOLLOWER_URL = "https://eksisozluk.com/takipci/"
        self.FOLLOWING_URL = "https://eksisozluk.com/takip/"
        self.driver = webdriver.Firefox()
    def __repr__(self) -> str:
        return f"Connection to the EksiSozluk with the Username\n{self.CREDENTIALS['user_name']}\nLogged In:{self.logged_in}"

    def login(self, robot_ = True):


        '''
        This is the principle function to login to the eksisozluk.com. The problem is 
        there will be a robot check with high probability. So if robot_ set to True,
        you need to check the box manually while signing in. Then pressing any key will keep the
        code running. 
        
        '''


        print('Logging in to the EksiSozluk.com')
        self.driver.get('https://eksisozluk.com/')
        sleep(3)

        ## Login
        try:
            self.driver.find_element('css selector','#top-login-link').click() #Click on the Login Page
            self.driver.find_element('css selector', '#username').send_keys(self.CREDENTIALS['user_name']) # Send Username
            self.driver.find_element('css selector', '#password').send_keys(self.CREDENTIALS['password']) # Send Password

            if robot_:
                input('Robot Check is Secured, Click on the Box then Press Any Button')
            self.driver.find_element('css selector', "button[class='btn btn-primary btn-lg btn-block']").click() # Click on Login
            print('Successfull Login')
            self.logged_in = True
            sleep(3)
        except:
            self.logged_in = False
            raise SystemError('Failure with the connection.')
    
    def get_user_info_basic(self, user_name)->dict:
        '''
        This function returns a dictionary of the users basic statistics.

        '''
        user_info = {}

        ## Go To The User Page
        self.driver.get(self.USER_URL + f'{user_name}')
        sleep(2)
        user_info['follower_count'] = self.driver.find_element(By.XPATH,'//*[@id="user-follower-count"]').text
        user_info['following_count']= self.driver.find_element(By.XPATH,'//*[@id="user-following-count"]').text
        user_info['total_entry_count'] = self.driver.find_element(By.XPATH,'//*[@id="entry-count-total"]').text

        return user_info
    
    def get_user_followers(self,user_name:str)->list:
        '''
        This function returns the followers as a list of a user as with their usernames in eksisozluk.com
        '''


        
        self.driver.get(self.FOLLOWER_URL + user_name)
        k = self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/div[2]/div[2]/section[1]/div[1]/ul[1]").text
        c = k.replace('\n',"")
        c = c.replace('takip et',';')
        c = c.split(';')
        c.pop()
        return c
    
    def get_user_following(self,user_name:str)->list:

        '''
        This function returns the users that a selected user follows as a list with ther usernames in eksisozluk.com
        '''
        self.driver.get(self.FOLLOWING_URL + user_name)
        k = self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/div[2]/div[2]/section[1]/div[1]/ul[1]").text
        c = k.replace('\n',"")
        c = c.replace('takip et',';')
        c = c.split(';')
        c.pop()
        return c 
    
