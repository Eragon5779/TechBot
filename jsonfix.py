import json

intel = json.loads(open('intel.json').read())
test = ""

for	cpu in intel['d'] :
	thing = str(cpu)[1328:]
	print(thing)
	thing =	thing.replace("None","null")
	thing =	thing.replace("True","true")
	thing =	thing.replace("False","false")
	thing = thing.replace('\'','"')
	test += '"' + str(cpu['ProductId']) + '": ' + '{' + thing + "},"

test = '{' + test[:-1] + '}'
print('\n\n\n\n\n\n\n\n')
print(test[:5298])
def pp_json(json_thing, sort=True, indents=4):
	if type(json_thing) is str:
		return(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
	else:
		return(json.dumps(json_thing, sort_keys=sort, indent=indents))
print(pp_json(test, False))