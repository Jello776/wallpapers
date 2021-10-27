import ctypes
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import urllib
import shutil
import requests
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
import os, os.path

def scroll_all(driver , scrolls = 1000):

	# To scroll a page a specific number of times controlled by scrolls
	SCROLL_PAUSE_TIME = 5
	count = 0
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		count += 1
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(SCROLL_PAUSE_TIME)
		new_height = driver.execute_script("return document.body.scrollHeight")

		if new_height == last_height:
			break
		if count == scrolls:
			break

		last_height = new_height


def new_window(driver):
	
	#To switch to a new window in order to save state on present window ( required to avoid stale element reference exception)
	WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
	driver.switch_to_window(driver.window_handles[1])
	time.sleep(7)


#------------------------------------------
def old_window(driver):

	# To switch back to previous state
	driver.switch_to_window(driver.window_handles[0])
	time.sleep(10)


def download_images(driver,image_links):

	loc = "F:/wallpapers"
	downloaded = 0
	for link in image_links:
		#new_window(driver)
		try:
			driver.get(link)
			time.sleep(2)

			now = datetime.now()
			dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
			#print dt_string
			image_name = "/" + dt_string + str(downloaded) + ".jpg"
			image_loc = loc + image_name
			
			temp = driver.find_element_by_xpath("//*[@id='media_container']/img")
			image_link = temp.get_attribute("src")
			print "new  :" + image_link
			response = requests.get(image_link, stream=True)
			with open(image_loc, 'wb') as out_file:
				shutil.copyfileobj(response.raw, out_file)
			del response
			downloaded += 1
			time.sleep(2)
		except:
			continue

		#old_window(driver)


def get_wallpapers():
	
	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_setting_values.notifications" : 2}
	chrome_options.add_experimental_option("prefs",prefs)
	driver = webdriver.Chrome(chrome_options=chrome_options)

	driver.get("https://pixabay.com/images/search/wallpaper/")
	time.sleep(10)

	page_no = 3 + random.randint(1,35)
	
	page = 0
	#cdpage_no = 0
	print page_no
	while page < page_no :
		page += 1
		driver.find_element_by_xpath("//*[@id='content']/div/a").click() # next page
		time.sleep(2)



	loc = "F:/wallpapers"

	scroll_all(driver,3)

	images = driver.find_elements_by_tag_name("a")

	start_from = random.randint(1,len(images))
	image_no = 0

	images_to_download = 25
	downloaded = 0

	image_links = []

	for image in images:
		try:
			image_link = image.get_attribute("href")
			#print image_link
			if "search" in image_link:
				continue
			if "photos" in image_link:
				print image_link
				image_links.append(image_link)
				downloaded += 1
				
		except:
			continue

		if downloaded == images_to_download:
			break

	download_images(driver,image_links)

	
def set_wallpaper():
	
	DIR = "F:/wallpapers"
	total_images = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
	print total_images
	#time.sleep(100)
	wallpaper = random.randint(1,total_images)
	number = 0

	for name in os.listdir(DIR):
		if os.path.isfile(os.path.join(DIR, name)) and number == wallpaper:
			break

		number += 1

	name = DIR + '/' + name
	print name
	ctypes.windll.user32.SystemParametersInfoA(0x14 , 10, name, 0x2)



get_wallpapers()

set_wallpaper()

# SPI_SETDESKWALLPAPER = 20 
# ctypes.windll.user32.SystemParametersInfoA(0x14 , 10, "F:/wallpapers/1.jpg" , 0x2)