import PyPDF2
import sys

class PdfExtractor:
    def __init__(self, pdf_file):
        self.pdfReader = PyPDF2.PdfFileReader(open(pdf_file, 'rb'))

    def get_headers(self):
        outline = self.pdfReader.getOutlines()
        result = list()

        for i in range(len(outline)):
            item = outline[i]
            ## checks for subheaders
            if isinstance(item, list):
                ## add subheader sections to result list as nested list
                self.helper(outline, i, result)
            else:
                ## add list containing header title, page number, text respectively to result list
                try:
                    toAdd = [item['/Title'], pdfReader.getDestinationPageNumber(item)]
                    result.append(toAdd)
                except:
                    continue

        self.generate_text(result)
        return result


    def helper(self, outline, index, res):

        new_list = list()
        res.append(new_list)

        subsections = outline[index]

        for i in range(len(subsections)):
            item = subsections[i]
            if isinstance(item, list):
                self.helper(subsections, i, new_list)
            else:
                try:
                    toAdd = [item['/Title'], pdfReader.getDestinationPageNumber(item)]
                    new_list.append(toAdd)
                except:
                    continue

    def generate_text(self, result):
        #print len(result)
        for i in range(len(result)):
            page_start = result[i][1]
            text = ''
            page_end = pdfReader.getNumPages()

            if i < len(result) - 1:
                page_end = result[i + 1][1]

            while page_start != page_end - 1:
                text += pdfReader.getPage(page_start).extractText()
                page_start += 1

            result[i].append(text)
