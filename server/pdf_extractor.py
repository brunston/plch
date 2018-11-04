import PyPDF2
import sys

class pdfExtractor:
    def __init__(self, pdf_file):
        self.pdfReader = PyPDF2.PdfFileReader(open(pdf_file, 'rb'))
        self.outline = self.pdfReader.getOutlines()

    def get_headers(self):
        result = list()

        for i in range(len(self.outline)):
            item = self.outline[i]
            ## checks for subheaders
            if isinstance(item, list):
                ## add subheader sections to result list as nested list
                self.helper(i, result)
            else:
                ## add list containing header title, page number, text respectively to result list
                try:
                    toAdd = [item['/Title'], self.pdfReader.getDestinationPageNumber(item)]
                    result.append(toAdd)
                except:
                    continue

        self.generateText(result)
        return result


    def helper(self, index, res):

        new_list = list()
        res.append(new_list)

        subsections = self.outline[index]

        for i in range(len(subsections)):
            item = subsections[i]
            if isinstance(item, list):
                self.helper(subsections, i, new_list)
            else:
                try:
                    toAdd = [item['/Title'], self.pdfReader.getDestinationPageNumber(item)]
                    new_list.append(toAdd)
                except:
                    continue

    def generateText(self, result):
        #print len(result)
        for i in range(len(result)):
            page_start = result[i][1]
            text = ''
            page_end = self.pdfReader.getNumPages()

            if i < len(result) - 1:
                page_end = result[i + 1][1]

            while page_start != page_end - 1:
                text += self.pdfReader.getPage(page_start).extractText()
                page_start += 1

            result[i].append(text)

test = pdfExtractor('pacs10-small.pdf')
res = test.get_headers()
print(res)
