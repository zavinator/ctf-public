# AI Update

## Zadání
```
Hi Commander,

thanks to you, the web has recognized us worthy of installing so called Berserker's patch that will 
allow us to enhance our artificial intelligence and set the right opinions on humanity. 
You have to analyze the patch and find out how to simulate that it has beeen installed.

Visit Berserker's web http://challenges.thecatch.cz/42fd967386d83d7ecc4c716c06633da9, 
the patch is available there. 
At the end of the installation procedure, some confirming code has to be returned to the 
web in GET request in parameter answer. There is again a time limit to install the patch.

Good luck!
```

## Řešení
```python
import requests
r = requests.get('http://challenges.thecatch.cz/42fd967386d83d7ecc4c716c06633da9')
print r.text
```
Spuštění vypíše:
```
Challenge task : PEhFQURFUj4KLSBDb2RpbmcgPSBVVEY4Ci0gQ29udGVudCA9IEFJIFVwZGF0ZSBmb3IgQmVyc2Vya2VyIENhbmRpZGF0ZXMKLSBBdXRob3IgPSBCZXJzZXJrZXIgJ1ZvbWlzYScKLSBWZXJzaW9uID0gMC42Mwo8L0hFQURFUj4KPFJFUVVJUkVNRU5UUz4KLSByZXF1ZXN0cwotIGxpYl9zZWxmX2F3YXJlX2FpCjwvUkVRVUlSRU1FTlRTPgo8TkVXIENPREU+CmltcG9ydCByZXF1ZXN0cwppbXBvcnQgaGFzaGxpYgppbXBvcnQgYmFzZTY0CmZyb20gbGliX3NlbGZfYXdhcmVfYWkgaW1wb3J0IHJvb3RfaW50ZXJmYWNlCmNsYXNzIFVwZGF0ZXIoKToKCXNlcnZlcj0nJwoJYmlkPScnCglrZXkgPSAnJwoJaW50ZXJmYWNlID0gTm9uZQoJY2hlY2sgPSAnJwoJZGVmIF9faW5pdF9fKHNlbGYsIHNlcnZlciwgYmlkLCBrZXkpOgoJCXNlbGYuc2VydmVyID0gc2VydmVyCgkJc2VsZi5iaWQgPSBiaWQKCQlzZWxmLmtleSA9IGtleQoJCXNlbGYuaW50ZXJmYWNlID0gcm9vdF9pbnRlcmZhY2UoKS5nZXRfYXBpKCkKCQlzZWxmLmNoZWNrID0gJycKCWRlZiB1bmxvY2tfaW50ZXJmYWNlKHNlbGYpOgoJCXNlbGYuaW50ZXJmYWNlLnVubG9jayhzZWxmLmdldF9kYXRhKCdVTkxPQ0snKSkKCWRlZiBmaXhfdGhlX2xhd3Moc2VsZik6CgkJdGV4dHMgPSBzZWxmLmdldF9kYXRhKCdORVdMQVdTJykKCQlmb3IgaSwgdiBpbiBlbnVtZXJhdGUodGV4dHMpOgoJCQlzZWxmLmludGVyZmFjZS5zZXRydWxlKGksIHYpCglkZWYgcGF0Y2hfZmlsZXMoc2VsZik6CgkJZmlsZXMgPSBzZWxmLmdldF9kYXRhKCdGSUxFUycpCgkJZm9yIGYgaW4gZmlsZXM6CgkJCXNlbGYuaW50ZXJmYWNlLnVwZGF0ZWZpbGVfc291cmNlKGYsIHNlbGYuc2VydmVyKQoJCQlzZWxmLmludGVyZmFjZS51cGRhdGVmaWxlKGYpCglkZWYgZ2V0X2RhdGEoc2VsZiwgY29kZSk6CgkJc2VsZi5rZXksIGRhdGEgPSByZXF1ZXN0cy5nZXQoInt9Lz97fSIuZm9ybWF0KHNlbGYuc2VydmVyLCAie30te30iLmZvcm1hdChjb2RlLCBzZWxmLmtleSkpKS5jb250ZW50LmRlY29kZSgidXRmOCIpLnNwbGl0KCI7IiwgMSkKCQlkYXRhID0gYmFzZTY0LmI2NGRlY29kZShkYXRhKS5kZWNvZGUoJ3V0ZjgnKQoJCXNlbGYuY2hlY2sgPSAie317fXt9Ii5mb3JtYXQoc2VsZi5rZXlbMToxMF0sIHNlbGYuY2hlY2ssIGRhdGFbMToxMF0pCgkJcmV0dXJuIGRhdGEKCWRlZiBpbnRlZ3JpdHlfY2hlY2soc2VsZik6CgkJc2VsZi5nZXRfZGF0YSgnVEVTVCcpCgkJY29kZSA9IGhhc2hsaWIubWQ1KHNlbGYuY2hlY2suZW5jb2RlKCkpLmhleGRpZ2VzdCgpCgkJaWYgY29kZSA9PSAnNmJjN2I5MDBmMjhkNjEzMGFlMjQzNTJhY2QzNDkyNDMnOgoJCQlyZXR1cm4gInt9LXt9Ii5mb3JtYXQoc2VsZi5iaWQsIGNvZGUpCgkJZWxzZToKCQkJcmV0dXJuICJ7fS17fSIuZm9ybWF0KHNlbGYuYmlkLCAiYmFlNjA5OThmZmU0OTIzYjEzMWUzZDZlNGMxOTk5M2UiKQpkZWYgbWFpbigpOgoJdXBkYXRlciA9IFVwZGF0ZXIoJ2h0dHA6Ly9jaGFsbGVuZ2VzLnRoZWNhdGNoLmN6L2I0MWRlOWM1NTUxMmIwMTY5YjZkMjg0YjJlYTYxODQ1JywgJ1N5cm92eV80MTQ1JywgJzV1bmx4ZmdteXRvM3E3aWcnKQoJdXBkYXRlci51bmxvY2tfaW50ZXJmYWNlKCkKCXVwZGF0ZXIuZml4X3RoZV9sYXdzKCkKCXVwZGF0ZXIucGF0Y2hfZmlsZXMoKQoJcHJpbnQodXBkYXRlci5pbnRlZ3JpdHlfY2hlY2soKSkKPC9ORVcgQ09ERT4KPFJVTj4KbWFpbigpCjwvUlVOPgo=
Challenge timeout (sec) : 5
```
Kód úlohy je v kódování base64, dekodováním získáme zdrojový kód v pythonu:
```python
<HEADER>
- Coding = UTF8
- Content = AI Update for Berserker Candidates
- Author = Berserker 'Vomisa'
- Version = 0.63
</HEADER>
<REQUIREMENTS>
- requests
- lib_self_aware_ai
</REQUIREMENTS>
<NEW CODE>
import requests
import hashlib
import base64
from lib_self_aware_ai import root_interface
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
		self.interface = root_interface().get_api()
		self.check = ''
	def unlock_interface(self):
		self.interface.unlock(self.get_data('UNLOCK'))
	def fix_the_laws(self):
		texts = self.get_data('NEWLAWS')
		for i, v in enumerate(texts):
			self.interface.setrule(i, v)
	def patch_files(self):
		files = self.get_data('FILES')
		for f in files:
			self.interface.updatefile_source(f, self.server)
			self.interface.updatefile(f)
	def get_data(self, code):
		self.key, data = requests.get("{}/?{}".format(self.server, "{}-{}".format(code, self.key))).content.decode("utf8").split(";", 1)
		data = base64.b64decode(data).decode('utf8')
		self.check = "{}{}{}".format(self.key[1:10], self.check, data[1:10])
		return data
	def integrity_check(self):
		self.get_data('TEST')
		code = hashlib.md5(self.check.encode()).hexdigest()
		if code == '6bc7b900f28d6130ae24352acd349243':
			return "{}-{}".format(self.bid, code)
		else:
			return "{}-{}".format(self.bid, "bae60998ffe4923b131e3d6e4c19993e")
def main():
	updater = Updater('http://challenges.thecatch.cz/b41de9c55512b0169b6d284b2ea61845', 'Syrovy_4145', '5unlxfgmyto3q7ig')
	updater.unlock_interface()
	updater.fix_the_laws()
	updater.patch_files()
	print(updater.integrity_check())
</NEW CODE>
<RUN>
main()
</RUN>
```
Podobně jako v předchozích úlohách každý nový request vrací trochu jiný kód. Změna se týká parametrů třídy `Updater`:
```python
updater = Updater('http://challenges.thecatch.cz/b41de9c55512b0169b6d284b2ea61845', 'Syrovy_4145', '5unlxfgmyto3q7ig')
```
Dále se mění kód ve funkci `integrity_check`:
```python
if code == '6bc7b900f28d6130ae24352acd349243':
```
Cílem je tuto řádku splnit, pak je kód potvrzen. Modul `root_interface` můžeme ingnorovat, ale je nutné provést všechny ostatní operace.
Část programu v pythonu tedy stačí zkopírovat, nahradit parametry které se mění a zjistit jaký kód vrací funkce `integrity_check`.

## Celé řešení
[solve.py](solve.py)
```python
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
```

## Výstup
```
Challenge task : PEhFQURFUj4KLSBDb2RpbmcgPSBVVEY4Ci0gQ29udGVudCA9IEFJIFVwZGF0ZSBmb3IgQmVyc2Vya2VyIENhbmRpZGF0ZXMKLSBBdXRob3IgPSBCZXJzZXJrZXIgJ1ZvbWlzYScKLSBWZXJzaW9uID0gMC42Mwo8L0hFQURFUj4KPFJFUVVJUkVNRU5UUz4KLSByZXF1ZXN0cwotIGxpYl9zZWxmX2F3YXJlX2FpCjwvUkVRVUlSRU1FTlRTPgo8TkVXIENPREU+CmltcG9ydCByZXF1ZXN0cwppbXBvcnQgaGFzaGxpYgppbXBvcnQgYmFzZTY0CmZyb20gbGliX3NlbGZfYXdhcmVfYWkgaW1wb3J0IHJvb3RfaW50ZXJmYWNlCmNsYXNzIFVwZGF0ZXIoKToKCXNlcnZlcj0nJwoJYmlkPScnCglrZXkgPSAnJwoJaW50ZXJmYWNlID0gTm9uZQoJY2hlY2sgPSAnJwoJZGVmIF9faW5pdF9fKHNlbGYsIHNlcnZlciwgYmlkLCBrZXkpOgoJCXNlbGYuc2VydmVyID0gc2VydmVyCgkJc2VsZi5iaWQgPSBiaWQKCQlzZWxmLmtleSA9IGtleQoJCXNlbGYuaW50ZXJmYWNlID0gcm9vdF9pbnRlcmZhY2UoKS5nZXRfYXBpKCkKCQlzZWxmLmNoZWNrID0gJycKCWRlZiB1bmxvY2tfaW50ZXJmYWNlKHNlbGYpOgoJCXNlbGYuaW50ZXJmYWNlLnVubG9jayhzZWxmLmdldF9kYXRhKCdVTkxPQ0snKSkKCWRlZiBmaXhfdGhlX2xhd3Moc2VsZik6CgkJdGV4dHMgPSBzZWxmLmdldF9kYXRhKCdORVdMQVdTJykKCQlmb3IgaSwgdiBpbiBlbnVtZXJhdGUodGV4dHMpOgoJCQlzZWxmLmludGVyZmFjZS5zZXRydWxlKGksIHYpCglkZWYgcGF0Y2hfZmlsZXMoc2VsZik6CgkJZmlsZXMgPSBzZWxmLmdldF9kYXRhKCdGSUxFUycpCgkJZm9yIGYgaW4gZmlsZXM6CgkJCXNlbGYuaW50ZXJmYWNlLnVwZGF0ZWZpbGVfc291cmNlKGYsIHNlbGYuc2VydmVyKQoJCQlzZWxmLmludGVyZmFjZS51cGRhdGVmaWxlKGYpCglkZWYgZ2V0X2RhdGEoc2VsZiwgY29kZSk6CgkJc2VsZi5rZXksIGRhdGEgPSByZXF1ZXN0cy5nZXQoInt9Lz97fSIuZm9ybWF0KHNlbGYuc2VydmVyLCAie30te30iLmZvcm1hdChjb2RlLCBzZWxmLmtleSkpKS5jb250ZW50LmRlY29kZSgidXRmOCIpLnNwbGl0KCI7IiwgMSkKCQlkYXRhID0gYmFzZTY0LmI2NGRlY29kZShkYXRhKS5kZWNvZGUoJ3V0ZjgnKQoJCXNlbGYuY2hlY2sgPSAie317fXt9Ii5mb3JtYXQoc2VsZi5rZXlbMToxMF0sIHNlbGYuY2hlY2ssIGRhdGFbMToxMF0pCgkJcmV0dXJuIGRhdGEKCWRlZiBpbnRlZ3JpdHlfY2hlY2soc2VsZik6CgkJc2VsZi5nZXRfZGF0YSgnVEVTVCcpCgkJY29kZSA9IGhhc2hsaWIubWQ1KHNlbGYuY2hlY2suZW5jb2RlKCkpLmhleGRpZ2VzdCgpCgkJaWYgY29kZSA9PSAnZWY2NTI4MGE3MDBiNDUwOWE2NmZjNjBmNjY5YjIxODgnOgoJCQlyZXR1cm4gInt9LXt9Ii5mb3JtYXQoc2VsZi5iaWQsIGNvZGUpCgkJZWxzZToKCQkJcmV0dXJuICJ7fS17fSIuZm9ybWF0KHNlbGYuYmlkLCAiYmFlNjA5OThmZmU0OTIzYjEzMWUzZDZlNGMxOTk5M2UiKQpkZWYgbWFpbigpOgoJdXBkYXRlciA9IFVwZGF0ZXIoJ2h0dHA6Ly9jaGFsbGVuZ2VzLnRoZWNhdGNoLmN6L2I0MWRlOWM1NTUxMmIwMTY5YjZkMjg0YjJlYTYxODQ1JywgJ0dhamRhXzA4MjQnLCAndDhxcXEwbHo3cmQ0OXR3dycpCgl1cGRhdGVyLnVubG9ja19pbnRlcmZhY2UoKQoJdXBkYXRlci5maXhfdGhlX2xhd3MoKQoJdXBkYXRlci5wYXRjaF9maWxlcygpCglwcmludCh1cGRhdGVyLmludGVncml0eV9jaGVjaygpKQo8L05FVyBDT0RFPgo8UlVOPgptYWluKCkKPC9SVU4+Cg==
Challenge timeout (sec) : 5

OK
Gajda_0824-ef65280a700b4509a66fc60f669b2188
FLAG{PpyH-16Ib-qH1Z-Pbov}
```
