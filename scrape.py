from PIL import Image
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from bs4 import BeautifulSoup
import xlrd
from os.path import expanduser
home = expanduser("~")

profile = webdriver.FirefoxProfile("/home/henry/.mozilla/firefox/ubjfmgc2.scraper")
driver = webdriver.Firefox(profile)

# driver = webdriver.Firefox()
driver.implicitly_wait(30)
url = "https://www.dndbeyond.com"
driver.get(url)
test = input("Press enter to continue")
print(test)

#Use to get list of monster names
loc = home + "/Touch-DnD/" + "Monster Spreadsheet (D&D5e).xlsx"
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 
mon_col = 0
sor_col = 20
start = 0
for m in range(start, 5):
	monster = sheet.cell_value(m, mon_col)
	source  = sheet.cell_value(m, sor_col)

	#only own the monster manual at this stage
	if source == "Monster Manual":
		print(source + " " + monster)

		comma_sep_monster = monster.split(",")
		if len(comma_sep_monster) > 1:
			monster = comma_sep_monster[len(comma_sep_monster) - 1]
		monster = monster.strip()

		space_sep_monster = monster.split(" ")
		if len(space_sep_monster) > 1:
			monster = space_sep_monster[0]
			for i in range(1, len(space_sep_monster)):
				monster += "-"+space_sep_monster[i]
		
		url = "https://www.dndbeyond.com/monsters/"+monster
		print(url)
		#TODO Wrap in try/catch to catch bad urls (bad URL format) and save so I can manually edit and run it
		# contents = opener.open(url)
		#launch url
		
		# create a new Firefox session
		driver.get(url)

		soup = BeautifulSoup(driver.page_source, 'html.parser')

		#From here strip out character details and save to file
		print("**************")
		print("**************")
		for tag in soup.find_all('div'):
			content = tag.get("class")
			
			if content is not None: 
				if content[0] == "mon-stat-block__description-block-content":
					print("**************")
					print(tag.text)	
				elif content[0] == "ability-block__data":
					print("**************")
					print(tag.text)
				elif content[0] == "mon-stat-block__tidbits":
					print("**************")
					print(tag.text)
				elif content[0] == "image":
					print("**************")
					for img in tag.find_all('img'):
						print(img['src'])
						img = Image.open(requests.get(img['src'], stream = True).raw)
						img.save(home+"/Touch-DnD/images/"+monster+".jpg")
				elif content[0] == "mon-stat-block__meta":
					print(tag.text)
	else:
		print("Don't own")
