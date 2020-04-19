# Customize these variables to define input and output
anobii_file = "anobii_export.csv"
goodreads_file = "import_to_goodreads.csv" 

# Customize language translations
FINISHED = "Finito nel "
DROPPED  = "Abbandonato nel "
READING  = "In lettura dal "
MONTHS   = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]

####### do not change anything below this line

from datetime import date
import csv, codecs, cStringIO

class UTF8Recoder:
	"""
	Iterator that reads an encoded stream and reencodes the input to UTF-8
	"""
	def __init__(self, f, encoding):
		self.reader = codecs.getreader(encoding)(f)
	
	def __iter__(self):
		return self
	
	def next(self):
		return self.reader.next().encode("utf-8")

class UnicodeReader:
	"""
	A CSV reader which will iterate over lines in the CSV file "f",
	which is encoded in the given encoding.
	"""
	
	def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
		f = UTF8Recoder(f, encoding)
		self.reader = csv.reader(f, dialect=dialect, **kwds)
	
	def next(self):
		row = self.reader.next()
		return [unicode(s, "utf-8") for s in row]
	
	def __iter__(self):
		return self

class UnicodeWriter:
	"""
	A CSV writer which will write rows to CSV file "f",
	which is encoded in the given encoding.
	"""
	
	def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
		# Redirect output to a queue
		self.queue = cStringIO.StringIO()
		self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
		self.stream = f
		self.encoder = codecs.getincrementalencoder(encoding)()

	def writerow(self, row):
		items = []
		for s in row:
			if type(s) == type(u"s"):
				items.append(s.encode("utf8"))
			else:
				items.append(s)

		self.writer.writerow(items)
		# Fetch UTF-8 output from the queue ...
		data = self.queue.getvalue()
		data = data.decode("utf-8")
		# ... and reencode it into the target encoding
		data = self.encoder.encode(data)
		# write to the target stream
		self.stream.write(data)
		# empty queue
		self.queue.truncate(0)

	def writerows(self, rows):
		for row in rows:
			self.writerow(row)


reader = UnicodeReader(open(anobii_file,"rb"))
reader.next() # first line is column titles
target = []
target.append(["Title","Author","Additional Authors","ISBN","ISBN13","My Rating","Average Rating","Publisher","Binding","Year Published","Original Publication Year","Date Read","Date Added","Bookshelves","My Review","Spoiler","Private Notes","Recommended For","Recommended By"])
# loading all in memory is not efficient, there's certainly a better way
for l in reader:
	# isbn
	isbn = l[0].replace("'","")
	# title
	if l[2] == "":
		title = l[1]
	else:
		title = l[1] + ". " + l[2]
	# author
	author = l[3]
	# binding
	binding = l[4]
	# pages
	pages = l[5]
	# publisher
	publisher = l[6]
	# pubdate
	pubdate = (l[7])[1:5]
	# privnote
	privnote = l[8]
	# comment
	comment = l[10]
	# status
	status = l[11]
	# bookshelves
	bookshelves = "to-read";
	if status.startswith(FINISHED): bookshelves = "read"
	if status.startswith(READING):  bookshelves = "currently-reading"
	if status.startswith(DROPPED):  bookshelves = "gave-up-on"
	# readdate
	tmpreaddate = l[11].replace(", 00:00:00","")
	yreaddate = tmpreaddate[-4:]
	mtmpreaddate = tmpreaddate.replace(yreaddate,"")[-5:]
	mreaddate = ""
	if mtmpreaddate.strip() == MONTHS[0]:  mreaddate = "01"
	if mtmpreaddate.strip() == MONTHS[1]:  mreaddate = "02"
	if mtmpreaddate.strip() == MONTHS[2]:  mreaddate = "03"
	if mtmpreaddate.strip() == MONTHS[3]:  mreaddate = "04"
	if mtmpreaddate.strip() == MONTHS[4]:  mreaddate = "05"
	if mtmpreaddate.strip() == MONTHS[5]:  mreaddate = "06"
	if mtmpreaddate.strip() == MONTHS[6]:  mreaddate = "07"
	if mtmpreaddate.strip() == MONTHS[7]:  mreaddate = "08"
	if mtmpreaddate.strip() == MONTHS[8]:  mreaddate = "09"
	if mtmpreaddate.strip() == MONTHS[9]:  mreaddate = "10"
	if mtmpreaddate.strip() == MONTHS[10]: mreaddate = "11"
	if mtmpreaddate.strip() == MONTHS[11]: mreaddate = "12"
	dtmpreaddate = tmpreaddate.replace(yreaddate,"").replace(mtmpreaddate,"")[-2:]
	dreaddate = dtmpreaddate.replace(" ","0")
	readdate = yreaddate + "-" + mreaddate + "-" + dreaddate
	if readdate == "1970-01-01": readdate = ""
	if readdate == "--": readdate = ""
	# dateadded
	dateadded = readdate
	# recover readdate basing on bookshelves
	if bookshelves == "currently-reading": readdate = ""
	if bookshelves == "gave-up-on": readdate = ""
	# rating
	rating = l[12]
	
	tline = [title,author,"",isbn,"",rating,"",publisher,binding,pubdate,"",readdate,dateadded,bookshelves,comment,"",privnote,"",""]
	target.append(tline)

writer = UnicodeWriter(open(goodreads_file,"wb"),dialect='excel',quoting=csv.QUOTE_NONNUMERIC)
writer.writerows(target)

print "Done! saved output to " + goodreads_file