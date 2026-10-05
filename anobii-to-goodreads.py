# Customize these variables to define input and output
anobii_file = "anobii_export.csv"
goodreads_file = "import_to_goodreads.csv" 

# Customize language translations
FINISHED = "Finished on "
DROPPED  = "Abandoned on "
READING  = "Reading since "
MONTHS   = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]

####### do not change anything below this line

from datetime import date
import csv, io, re

# Anobii exports text as UTF-16 code units but delimiters as single bytes: drop the NUL bytes
data = open(anobii_file, "rb").read().replace(b"\x00", b"")
try:
	data = data.decode("utf-8")
except UnicodeDecodeError:
	data = data.decode("latin-1")
reader = csv.reader(io.StringIO(data, newline=""))
next(reader) # first line is column titles
target = []
target.append(["Title","Author","Additional Authors","ISBN","ISBN13","My Rating","Average Rating","Publisher","Binding","Year Published","Original Publication Year","Date Read","Date Added","Shelves","Bookshelves","My Review","Spoiler","Private Notes","Recommended For","Recommended By"])
# loading all in memory is not efficient, there's certainly a better way
for l in reader:
	# isbn
	isbn = l[0].replace("'","")
	if isbn is None or isbn == "":
		print("Invalid ISBN in '" + l[1] + "' book, consider adding it manually")
		continue
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
	pubdate = (l[7])[0:4]
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
	# ISO dates, possibly partial (YYYY or YYYY-MM): missing month/day default to 01
	isodate = re.search(r"(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$", tmpreaddate)
	if isodate: readdate = isodate.group(1) + "-" + (isodate.group(2) or "01") + "-" + (isodate.group(3) or "01")
	if readdate == "1970-01-01": readdate = ""
	if readdate == "--": readdate = ""
	# dateadded
	dateadded = readdate
	# recover readdate basing on bookshelves
	if bookshelves == "currently-reading": readdate = ""
	if bookshelves == "gave-up-on": readdate = ""
	# rating
	rating = l[12]
	
	tline = [title,author,"",isbn,"",rating,"",publisher,binding,pubdate,"",readdate,dateadded,bookshelves,bookshelves,comment,"",privnote,"",""]
	target.append(tline)

writer = csv.writer(open(goodreads_file, "w", encoding="utf-8", newline=""),dialect='excel',quoting=csv.QUOTE_NONNUMERIC)
writer.writerows(target)

print("Done! saved output to " + goodreads_file)