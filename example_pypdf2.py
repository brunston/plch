import PyPDF2
import pprint

pprinter = pprint.PrettyPrinter().pprint

pdf = open('ee16a-reader.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdf)

outline = pdfReader.getOutlines()

first_chapter = pdfReader.getDestinationPageNumber(outline[0])

##pprinter(outline[0])

#pprinter(first_chapter)

pprinter(outline[1])
##pprinter(outline)
