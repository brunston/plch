import PyPDF2
from PyPDF2_pdf_patch import extractText_patch
import os

PyPDF2.pdf.PageObject.extractText = extractText_patch

def get_pdf_file_in_texts(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    final_file_path = os.path.join(dir_path, "../texts/" + file_name)
    return final_file_path


class DestinationWrapper:
    def __init__(self, destination_obj, parent_str = ""):
        self.dest = destination_obj
        self.parent_string = parent_str
        self.text = None

    def add_parent(self, s):
        self.parent_string += (" -> " + s) if self.parent_string else s

    def set_text(self, text):
        self.text = text

    def get_title(self):
        return self.parent_string + " -> " + self.dest['/Title'] if self.parent_string else str(self.dest['/Title'])


class PdfExtractor:
    def __init__(self, pdf_file):
        PyPDF2.pdf.PageObject.extractText = extractText_patch
        self.pdfReader = PyPDF2.PdfFileReader(open(pdf_file, 'rb'))
        self.outline = self.pdfReader.getOutlines()

    def get_corpus_pages_headers(self):
        """
        :return: corpus, pages, headers
        matching indexes -> corpus[i] = text // pages[i] = starting page number // headers[i] = section title
        """
        unnested_destWs = list() # ordered list of subsections
        parent_strings = [""]
        def wrp_dest_to_dests(nested_list, pop=False):
            if not nested_list: # base case is the empty list
                parent_strings.pop()  # go back to old parent string
                return
            elif isinstance(nested_list, list):
                if pop:
                    # this means the previous header was the parent section
                    parent = unnested_destWs.pop()
                    parent_strings.append(parent.get_title()) # new parent string
                wrp_dest_to_dests(nested_list[0], pop=True)
                wrp_dest_to_dests(nested_list[1:], pop=False)
            else:
                unnested_destWs.append(DestinationWrapper(nested_list, parent_str= parent_strings[-1]))
        wrp_dest_to_dests(self.outline, pop=False)
        self.generate_text(unnested_destWs)
        corpus = [destW.text for destW in unnested_destWs if destW.text]
        pages = [self.pdfReader.getDestinationPageNumber(destW.dest) for destW in unnested_destWs if destW.text]
        headers = [destW.get_title() for destW in unnested_destWs if destW.text]
        return corpus, pages, headers

    def generate_text(self, unnested_destWs):
        #print len(result)
        page_starts = [self.pdfReader.getDestinationPageNumber(destW.dest) for destW in unnested_destWs] + \
                      [self.pdfReader.getNumPages()]
        for i in range(len(unnested_destWs)):
            page_start = page_starts[i]
            page_end = page_starts[i+1]
            text = ''
            while page_start < page_end:
                text += self.pdfReader.getPage(page_start).extractText()
                page_start += 1
            unnested_destWs[i].set_text(text)

if __name__ == '__main__':
    path = get_pdf_file_in_texts("reinforcement-an-introduction.pdf")
    p = PdfExtractor(path)
    corpus, pages, headers = p.get_corpus_pages_headers()
    print(pages)
    print(headers)
    for text in corpus:
        print(text)
        input("get more? <Enter>")
    print("done")
