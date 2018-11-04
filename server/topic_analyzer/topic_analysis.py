import server.topic_analyzer.pdf_extractor as pdf_extractor
from gensim import corpora, models, similarities
import ast

class TopicAnalyzer:
    def __init__(self, pdf_file):
        self.extractor = pdf_extractor.PdfExtractor(pdf_file)

if __name__=="__main__":
    import pprint
    pprinter = pprint.PrettyPrinter().pprint
    analyzer = TopicAnalyzer("pacs10-small.pdf")
    topic_list = analyzer.extractor.get_corpus_pages_headers()
    #pprinter(topic_list[1])
    topic_list = []
    with open('cleanest_pacs.txt') as f:
        topic_list = ast.literal_eval(f.read())
    stoplist = set('for a of the and to in have was is or it has are on each fine one were me my her she he his their they them these (p.'.split())
    texts = [[word for word in str(document).lower().split() if word not in stoplist] for document in topic_list]
    #pprinter(texts)
    dictionary = corpora.Dictionary(texts)
    #print(dictionary.token2id)
    #dictionary.save('pacs_corpora.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    #corpora.MmCorpus.serialize('pacs_corpus.mm', corpus) # save to disk
    tfidf = models.TfidfModel(corpus) # initialize a model
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
    corpus_lsi = lsi[corpus_tfidf]
    pprinter(lsi.print_topics(2))
    for doc in corpus_lsi:
        print(doc)
