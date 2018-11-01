from requests import request
import json
import importlib
from bs4 import BeautifulSoup

def build_template_for_year_day(year, day):
	pass

with open('config.json') as f:
	config = json.load(f)

year = 2017
day = 1

url = f'https://adventofcode.com/{year}/day/{day}'
res = request('GET',url,cookies=config)
with open(f'descriptions/aoc{year}day{day}.text','w') as f:
	soup = BeautifulSoup(res.text,'html.parser')
	f.write(soup.article.text)
	print(soup.article.text)
	
url = f'https://adventofcode.com/{year}/day/{day}/input'
res = request('GET',url,cookies=config)
with open(f'inputs/aoc{year}day{day}.in','wb') as f:
	for chunk in res.iter_content(chunk_size=128):
		f.write(chunk)

#lets do this thing
		
with open(f'descriptions/aoc{year}day{day}.text','r') as f:
	soup = BeautifulSoup(f.read(),'html.parser')
	

try:
	aoc_module = importlib.import_module(f'aoc{year}.day{day}')
	aoc_module.problem1('input')
	aoc_module.problem2('input')
except:
	build_template_for_year_day(year,day)
	print("caught")
	
