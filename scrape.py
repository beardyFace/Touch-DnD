import urllib.request
from bs4 import BeautifulSoup
import xlrd
from os.path import expanduser
home = expanduser("~")


# https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()

#Use to get list of monster names
loc = home + "/Scrape/" + "Monster Spreadsheet (D&D5e).xlsx"
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 
mon_col = 0
sor_col = 20
for m in range(1, 20):
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
		contents = opener.open(url)

		soup = BeautifulSoup(contents.read(), 'html.parser')

		#From here strip out character details and save to file
		for tag in soup.find_all('div'):
			content = tag.get("class")
			if content is not None: 
				if content[0] == "mon-stat-block__description-block-content":
					print("**************")
					print(tag.text)	
	else:
		print("Don't own")
