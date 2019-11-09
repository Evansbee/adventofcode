import re

def helpers_working():
	print("Helpers are working")
	
	
def wrap_to_count(the_string, characters):
	start = 0
	idx = start + characters
	while idx < len(the_string):
		while the_string[idx] != ' ' and idx > start:
			idx-=1
		the_string = the_string[:idx] + '\n' + the_string[idx+1:]
		idx += characters
	return the_string
	
#get rid of the n
def only_or_array(foo):
	if len(foo) == 1:
		return foo[0].strip('\n')
	return [x.strip('\n') for x in foo]

def get_numbers(in_string):
	return [int(x) for x in re.findall('[-+]?[0-9]+',in_string)]