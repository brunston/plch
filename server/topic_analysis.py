import pdf_extractor
from gensim import corpora, models, similarities
import pandas


class TopicAnalyzer:
    def __init__(self, pdf_file):
        self.extractor = pdf_extractor.PdfExtractor(pdf_file)

if __name__=="__main__":
    import pprint
    pprinter = pprint.PrettyPrinter().pprint
    analyzer = TopicAnalyzer("pacs10-small.pdf")
    topic_list = analyzer.extractor.get_headers()
    #pprinter(topic_list)
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in str(document).lower().split() if word not in stoplist] for document in topic_list]
    #pprinter(texts)
    dictionary = corpora.Dictionary(texts)
    #print(dictionary.token2id)
    #dictionary.save('pacs_corpora.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    #corpora.MmCorpus.serialize('pacs_corpus.mm', corpus) # save to disk
    tfidf = models.TfidfModel(corpus) # initialize a model
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
    corpus_lsi = lsi[corpus_tfidf]
    pprinter(lsi.print_topics(300))
