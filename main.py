from importlib.metadata import files
import os
import time
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def new_ep(f, ep_num):
	with open(f.name, "r") as t:
		file_nums = t.read()
		file_nums = file_nums.split('\n')
		for i in range(0, len(file_nums)):
			if file_nums[i] == str(ep_num):
				return False
	return True


def download_anime():
	path = "C:\\Users\\r2fpdvzocm5ydw\\PycharmProjects\\AnimeDownloader\\Anime_Files"
	files, flags = [], []
	anime_names = open(os.path.join(path, "anime_names.txt"), "r")
	anime_names = anime_names.read()
	anime_names = anime_names.split('\n')
	for anime in anime_names:
		f = open(os.path.join(path, anime + ".txt"), "a")
		files.append(f)
		flags.append(False)
	new_ep_found = True
	time.sleep(3)
	
	for j, anime in enumerate(anime_names):
		search = driver.find_element(By.CLASS_NAME, 'search-bar')
		search.clear()
		search.send_keys(anime + " asw")
		search.send_keys(Keys.RETURN)
		names = driver.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
		for i in range(0, len(names)):
			name = names[i].text[names[i].text.find(anime_names[j]):]
			nums = [int(s) for s in name.split() if s.isdigit()]
			ep_num = int(nums[0])

			if name.lower().find(anime_names[j].lower()) != -1:
				flags[j] = True
				new_ep_found = new_ep(files[j], ep_num)

			if new_ep_found:
				anime = names[i].find_elements(By.TAG_NAME, 'td')
				links = anime[2].find_elements(By.TAG_NAME, 'a')
				links[1].click()
				print("Clicked on the magnet link of " + name)
				files[j].write(str(ep_num) + "\n")
		files[j].close()
	
	if not new_ep_found:
		current_time = datetime.now().strftime("%H:%M:%S")
		print("No new ep released - " + current_time)


os.environ['WDM_LOG_LEVEL'] = '0'
os.environ['WDM_LOCAL'] = '1'
options = webdriver.ChromeOptions()
appdata = os.getenv('LOCALAPPDATA')
profile_path = os.path.join(appdata, "Google\\Chrome\\User Data")
options.add_argument(r"--user-data-dir=" + profile_path) #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument('--profile-directory=Profile 1') #e.g. Profile 3
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.maximize_window()
url = "https://nyaa.si/"

while not False:
	driver.get(url)
	download_anime()
	time.sleep(1200)

driver.close()