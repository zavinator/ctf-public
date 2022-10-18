import requests, re
import hashlib
import base64
#from lib_self_aware_ai import root_interface
class Updater():
	server=''
	bid=''
	key = ''
	interface = None
	check = ''
	def __init__(self, server, bid, key):
		self.server = server
		self.bid = bid
		self.key = key
		#self.interface = root_interface().get_api()
		self.check = ''
	def unlock_interface(self):
		self.get_data('UNLOCK')
		#self.interface.unlock(self.get_data('UNLOCK'))
	def fix_the_laws(self):
		texts = self.get_data('NEWLAWS')
		#for i, v in enumerate(texts):
		#	self.interface.setrule(i, v)
	def patch_files(self):
		files = self.get_data('FILES')
		#for f in files:
		#	self.interface.updatefile_source(f, self.server)
		#	self.interface.updatefile(f)
	def get_data(self, code):
		self.key, data = requests.get("{}/?{}".format(self.server, "{}-{}".format(code, self.key))).content.decode("utf8").split(";", 1)
		data = base64.b64decode(data).decode('utf8')
		self.check = "{}{}{}".format(self.key[1:10], self.check, data[1:10])
		return data
	def integrity_check(self, c):
		self.get_data('TEST')
		code = hashlib.md5(self.check.encode()).hexdigest()
		if code == c:
			print 'OK'		    
			return "{}-{}".format(self.bid, code)
		else:
			print 'WRONG'		    
			return "{}-{}".format(self.bid, "bae60998ffe4923b131e3d6e4c19993e")
			
def main(server, bid, key, code):
	updater = Updater(server, bid, key)
	updater.unlock_interface()
	updater.fix_the_laws()
	updater.patch_files()
	return updater.integrity_check(code)
	

r = requests.get('http://challenges.thecatch.cz/42fd967386d83d7ecc4c716c06633da9')
print r.text

src = base64.b64decode(re.search('Challenge task : (.*)', r.text).group(1))
server, bid, key = re.findall("'([^']*)'", re.search('updater = Updater\((.*)\)', src).group(1))
code = re.search("if code == '(.*)'", src).group(1)

check = main(server, bid, key, code)
print check

r = requests.get('http://challenges.thecatch.cz/42fd967386d83d7ecc4c716c06633da9/?answer='+check, cookies=r.cookies)
print r.text

