import glob
import sys
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def pdf_scrape(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 1
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    string = retstr.getvalue()
    retstr.close()
    return string

if len(sys.argv) != 2:
    print "\nERRORE: necessario inserire il path della directory come parametro"
    sys.exit()

if not os.path.exists(sys.argv[1]):
    print "\nERRORE: la directory specificata non esiste"
    sys.exit()

elenco = glob.glob(os.path.join(sys.argv[1],"*.pdf"))
print "Numero di file pdf nella cartella: " + str(len(elenco))

of = file(os.path.join(sys.argv[1], "index.txt"), "w")
for f in elenco:
    of.write(os.path.basename(f) + ";" + pdf_scrape(f).split()[0] + "\n")
of.close()
