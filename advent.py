from requests import request
import json
import importlib
from bs4 import BeautifulSoup
import datetime
from colorama import init, Fore, Back, Style
from helpers import *
import sys
import time
import os

def build_template_for_year_day(year, day):
	pass

with open('config.json') as f:
	config = json.load(f)

def get_most_recent_day_year():
	now = datetime.datetime.now()
	year = now.year
	day = now.day
	if now.month < 12:
		year = year - 1
		day = 25
	
	if now.day > 25:
		day = 25

	return day, year

def trim_to(the_text,columns):
	return the_text

def get_problem_text(day, year):
	url = f'https://adventofcode.com/{year}/day/{day}'
	res = request('GET',url,cookies=config)
	output = ""
	with open(f'descriptions/aoc{year}day{day}.text','w') as f:
		soup = BeautifulSoup(res.text,'html.parser')

		for article in soup.find_all('article'):
			f.write(article.text)
			output += article.text

		
		return all_of_them.wrap_to_count(output,120)
	

def get_input(day, year):
	if os.path.exists(f'inputs/aoc{year}day{day}.in'):
		with open(f'inputs/aoc{year}day{day}.in', 'r') as f:
			return f.readlines()
	else:
		url = f'https://adventofcode.com/{year}/day/{day}/input'
		res = request('GET',url,cookies=config)
		with open(f'inputs/aoc{year}day{day}.in','wb') as f:
			for chunk in res.iter_content(chunk_size=128):
				f.write(chunk)
		with open(f'inputs/aoc{year}day{day}.in','r') as f:
			return f.readlines()


if __name__ == '__main__':
	init()
	day, year = get_most_recent_day_year()


	if len(sys.argv) >= 2:
		day = sys.argv[1]
		print(f"Forcing Day {day}...")

	if len(sys.argv) >= 3:
		year = sys.argv[2]
		print(f"Forcing Year {year}...")


	try:
		print(f'AOC {year} Day {day}')
		problem_input = all_of_them.only_or_array(get_input(day,year))
		aoc_module = importlib.import_module(f'aoc{year}.day{day}')
		
		t0 = time.time()
		result1 = aoc_module.problem1(problem_input)
		t1 = time.time()

		result1_time = t1 - t0
		if result1:
			print(Fore.GREEN + f'Day {day} Problem 1 Result ' + Fore.BLUE + f'(Computed in {result1_time:0.2f}s): ' + Fore.RESET + f'{result1}')
		else:
			print(Fore.RED + f'Day {day} Problem 1 Result: ' + Fore.RESET + 'unknown...')
		t0 = time.time()
		result2 = aoc_module.problem2(problem_input)
		t1 = time.time()
		result1_time = t1 - t0
		if result2 is not None:
			print(Fore.GREEN + f'Day {day} Problem 2 Result ' + Fore.BLUE + f'(Computed in {result1_time:0.2f}s): ' + Fore.RESET + f'{result2}')
		else:
			print(Fore.RED + f'Day {day} Problem 2 Result: ' + Fore.RESET + 'unknown...')

	except Exception as e:
		print(e)
		build_template_for_year_day(year,day)
		
