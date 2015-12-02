from jsonschema import validate
import json

with open('user_config.json') as inf:
    data = json.load(inf)

with open('user_config_validator.json') as inf:
    config = json.load(inf)

print "data = " + str(data)
print "config = " + str(config)

print validate(data, config)
