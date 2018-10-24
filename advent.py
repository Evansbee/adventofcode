from requests import request
import json

with open('config.json') as f:
	config = json.load(f)

url = f'https://adventofcode.com/2017/day/1'
res = request('GET',url,cookies=config)
with open(f'tehinput.text','wb') as f:
	for chunk in res.iter_content(chunk_size=128):
		f.write(chunk)
	
url = f'https://adventofcode.com/2017/day/1/input'
res = request('GET',url,cookies=config)
with open(f'tehinput.in','wb') as f:
	for chunk in res.iter_content(chunk_size=128):
		f.write(chunk)
