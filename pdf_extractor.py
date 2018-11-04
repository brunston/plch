import PyPDF2
import sys

def get_headers(pdf_file):
    pdfReader = PyPDF2.PdfFileReader(open(pdf_file, 'rb'))
    outline = pdfReader.getOutlines()
    result = list()

    for i in range(len(outline)):
        item = outline[i]
        ## checks for subheaders
        if isinstance(item, list):
            ## add subheader sections to result list as nested list
            helper(outline, i, pdfReader, result)
        else:
            ## add list containing header title, page number, text respectively to result list
            try:
                toAdd = [item['/Title'], pdfReader.getDestinationPageNumber(item)]
                result.append(toAdd)
            except:
                continue

    generateText(result, pdfReader)
    return result


def helper(outline, index, pdfReader, res):

    new_list = list()
    res.append(new_list)

    subsections = outline[index]

    for i in range(len(subsections)):
        item = subsections[i]
        if isinstance(item, list):
            helper(subsections, i, pdfReader, new_list)
        else:
            try:
                toAdd = [item['/Title'], pdfReader.getDestinationPageNumber(item)]
                new_list.append(toAdd)
            except:
                continue

def generateText(result, pdfReader):
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
# if __name__ == "__main__":
#     pdf_file = sys.argv[1]
#     red = get_header(pdf_file)
#     return res
res = get_headers('pacs10-small.pdf')
print(res)
