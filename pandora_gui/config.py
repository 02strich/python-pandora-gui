import ConfigParser
import string

config = ConfigParser.SafeConfigParser()
config.read('config.ini')
for section in config.sections():
	for option in config.options(section):
		name = string.upper("%s_%s" % (section, option))
		#setattr(__package__, name, config.get(section, option))
		vars()[name] = config.get(section, option)