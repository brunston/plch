import pdf_extractor
import pandas


class TopicAnalyzer:
    def __init__(self, pdf_file):
        self.extractor = pdf_extractor.PdfExtractor(pdf_file)

if __name__=="__main__":
    import pprint
    pprinter = pprint.PrettyPrinter().pprint
    analyzer = TopicAnalyzer("pacs10-small.pdf")
    topic_list = analyzer.extractor.get_headers()
    pprinter(topic_list)
