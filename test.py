from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os

#launch url
url = "https://www.dndbeyond.com/monsters/orc"

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

#From here strip out character details and save to file
for tag in soup.find_all('div'):
	content = tag.get("class")
	
	if content is not None: 
		# if content[0] == "mon-stat-block__description-block-content":
		# 	print("**************")
		# 	print(tag.text)	
		# elif content[0] == "ability-block__data":
		# 	print(tag.text)
		# elif content[0] == "mon-stat-block__tidbits":
		# 	print(tag.text)
		if content[0] == "image":
			# print(content[0])
			print("******************")
			for img in tag.find_all('img'):
				print(img['src'])
			# print(tag)
			# img = Image.open(requests.get(image_url, stream = True).raw)
			# img.save('image.jpg')