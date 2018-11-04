import PyPDF2
import sys

def get_headers(pdf_file):
    pdfReader = PyPDF2.PdfFileReader(open(pdf_file, 'rb'))
    outline = pdfReader.getOutlines()
    result = list()

    for i in range(len(outline)):
        item = outline[i]
        print (item)
        ## checks for subheaders
        if isinstance(item, list):
            ## add subheader sections to result list as nested list
            helper(outline, i, pdfReader, result)
        else:
            ## add list containing header title, page number, text respectively to result list
            toAdd = [item['/Title'], pdfReader.getDestinationPageNumber(item)]
            result.append(toAdd)

    return result


def helper(outline, index, pdfReader, res):

    new_list = list()
    res.append(new_list)

    subsections = outline[index]

    for i in range(len(subsections)):
        item = subsections[i]
        print(item)
        if isinstance(item, list):
            helper(subsections, i, pdfReader, new_list)
        else:
            toAdd = [item['/Title'], pdfReader.getDestinationPageNumber(item)]
            new_list.append(toAdd)



# if __name__ == "__main__":
#     pdf_file = sys.argv[1]
#     red = get_header(pdf_file)
#     return res
get_headers('pacs10-small.pdf')
