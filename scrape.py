from PIL import Image
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import xlrd
from os.path import expanduser
# home = expanduser("~")
home = "E:\\Projects"
home += "\\Touch-DnD\\"

def handleDescription(tag):
    txt = "Description"
    descriptions = tag.findAll("div", {"class", "mon-stat-block__description-block"})
    for description in descriptions:
        labels  = description.findAll("div", {"class", "mon-stat-block__description-block-heading"})
        if len(labels) > 0:
            txt += labels[0].text
        content = description.findAll("div", {"class", "mon-stat-block__description-block-content"})[0]
        txt += content.text
    return txt + "\n"

def handleStatBlock(tag):
    # Base Stats 
    txt = "Stat-Block\n"
    stat_block = tag.findAll("div", {"class", "ability-block"})[0]
    stat_block = stat_block.findAll("div", {"class", "ability-block__stat"})
    for stat in stat_block:
        heading = stat.findAll("div", {"class", "ability-block__heading"})[0]
        data    = stat.findAll("div", {"class", "ability-block__data"})[0]
        txt += formatTxt(heading.text.encode("utf-8")) + " " + formatTxt(data.text.encode("utf-8")) + " "
    return txt + "\n\n"

def handleTidBits(tag):
    txt = "Traits\n"
    tidbits = tag.findAll("div", {"class", "mon-stat-block__tidbit"})
    for tidbit in tidbits:
        txt  += formatTxt(tidbit.text.encode("utf-8")) + "\n"
    # print(txt.encode("utf-8"))
    return txt + "\n"

def handleHeaders(tag):
    txt  = "Headers\n"
    meta = tag.findAll("div", {"class", "mon-stat-block__meta"})[0]
    txt += formatTxt(meta.text.encode("utf-8")) + "\n"
    # print(txt.encode("utf-8"))
    return txt + "\n"

def handleAttributes(tag):
    txt = "Attributes\n"
    attributes = tag.findAll("div", {"class", "mon-stat-block__attribute"})
    for attribute in attributes:
        txt  += formatTxt(attribute.text.encode("utf-8")) + "\n"
    # print(txt.encode("utf-8"))
    return txt + "\n"

def handleInfo(tag):
    txt = "Info\n"
    txt += tag.text.strip('\n')
    return txt

def formatTxtChar(txt, strip_char):
    txt_split = txt.split(strip_char)
    txt = txt_split[0]
    for i in range(1, len(txt_split)):
        if txt_split[i] is not "":
            txt += " " + txt_split[i]
    txt = txt.strip()
    return txt

def formatTxt(txt):
    txt = txt.decode('utf-8')
    txt = formatTxtChar(txt, "\n")
    txt = formatTxtChar(txt, " ")
    return txt
    
path = home + "geckodriver.exe"
profile = webdriver.FirefoxProfile("C:\\Users\\Henry\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\15zi4ing.scraper")
driver = webdriver.Firefox(profile, executable_path=path)

# driver = webdriver.Firefox()
driver.implicitly_wait(30)
url = "https://www.dndbeyond.com"
driver.get(url)
test = input("Press enter to continue")
print(test)

#Use to get list of monster names
loc = home + "Monster Spreadsheet (D&D5e).xlsx"

# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0)
  
# For row 0 and column 0 
mon_col = 0
sor_col = 20
start = 1
index = start

fail_path  = home + "monsters\\fails.txt"
fails_file = open(fail_path,'w', encoding="utf-8")
while sheet.cell_value(index, mon_col) is not "":
    monster = sheet.cell_value(index, mon_col)
    sheet_name = monster
    source  = sheet.cell_value(index, sor_col)
    index += 1

    #only own the monster manual at this stage
    print(source + " " + monster)
    if source == "Monster Manual":
        comma_sep_monster = monster.split(",")
        if len(comma_sep_monster) > 1:
            monster = comma_sep_monster[len(comma_sep_monster) - 1]
        monster = monster.strip()

        space_sep_monster = monster.split(" ")
        if len(space_sep_monster) > 1:
            monster = space_sep_monster[0]
            for i in range(1, len(space_sep_monster)):
                monster += "-"+space_sep_monster[i]
        monster = monster.replace('/', '-')

        file_path = home + "monsters\\" + monster + ".txt"
        stat_file = open(file_path,'w', encoding="utf-8")
        stat_file.write(monster+"\n\n")

        url = "https://www.dndbeyond.com/monsters/"+monster
        print(url)
        #TODO Wrap in try/catch to catch bad urls (bad URL format) and save so I can manually edit and run it
        # contents = opener.open(url)
        #launch url
        
        # create a new Firefox session
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        #From here strip out character details and save to file
        txt = ""
        for tag in soup.find_all('div'):
            content = tag.get("class")
            
            if content is not None: 
                if content[0] == "mon-stat-block":
                    for block_tag in tag.find_all('div', recursive=False):
                        # Actions/Abilities
                        block_content = block_tag.get('class')
                        # print(block_content)
                        # ['mon-stat-block__header']
                        # ['mon-stat-block__separator']
                        # ['mon-stat-block__attributes']
                        # ['mon-stat-block__stat-block']
                        # ['mon-stat-block__tidbits']
                        # ['mon-stat-block__separator']
                        # ['mon-stat-block__description-blocks']
                        # txt = ""
                        if block_content[0] == "mon-stat-block__description-blocks":
                            print("description")
                            txt += handleDescription(block_tag)

                        elif block_content[0] == "mon-stat-block__stat-block":
                            print("stat-block")
                            txt += handleStatBlock(block_tag)

                        # Resistences and such
                        elif block_content[0] == "mon-stat-block__tidbits":
                            print("tidbits")
                            txt += handleTidBits(block_tag)

                        # Size, alignment
                        elif block_content[0] == "mon-stat-block__header":
                            print("headers")
                            txt += handleHeaders(block_tag)
                        # AC/HP/Speed
                        elif block_content[0] == "mon-stat-block__attributes":
                            print("attributes")
                            txt += handleAttributes(block_tag)

                # Content
                elif content[0] == "more-info-content":
                    print("info")
                    txt += handleInfo(tag) + "\n"
            
                elif content[0] == "image":
                    print("image")
                    for img in tag.find_all('img'):
                        # print(img['src'])
                        image_url = img['src']
                        if not image_url.startswith("https:"):
                            image_url = "https:" + image_url
                        print(image_url)

                        try:
                            img = Image.open(requests.get(image_url, stream = True).raw)
                        except Exception as e:
                            print("Failed to load image")

                        def fixExt(ext):
                            if ext == "jpeg":
                                ext = ".jpg"
                            return ext

                        image_file = home+"images\\"+monster+fixExt(image_url[-4:])
                        # print(image_file)
                        img.save(image_file)

        if txt == "":
            fails_file.write(sheet_name+" -- "+monster+"\n")
            print("Failed to load: "+sheet_name+"\n"+monster)
        stat_file.write(txt)
        stat_file.close()
    else:
        print("Don't own")

fails_file.close()

