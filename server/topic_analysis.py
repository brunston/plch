import pdf_extractor as pdf_extractor
# import gensim
from gensim import corpora, models, similarities
# make a custom tokenizer
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer

class TopicAnalyzer:
    def __init__(self, pdf_file):
        self.extractor = pdf_extractor.PdfExtractor(pdf_file)

        #text scrapping from pdf
        self.raw_corpus, self.pages, self.headers = self.extractor.get_corpus_pages_headers()
        # bpbpbp: pages -> docid
        # bpbpbp: headings -> headings

        # get stop words
        nltk.download("stopwords")
        stoplist = set(stopwords.words('english'))

        # process raw_corpus (ie. list of strings)
        tokenizer = RegexpTokenizer('\w[\w-]*|\d(?:\d|,\d|\.\d)*') #any word with hyphens or number with decimal/commas
        t_corpus = [tokenizer.tokenize(s.lower()) for s in self.raw_corpus] #tokenized corpus


        # find bigrams (phrases of 2 words)
        bigram_ct = models.Phrases(t_corpus, common_terms=stoplist)

        # for all bigrams in t_corpus, combine into 1 word
        t_corpus = bigram_ct[t_corpus]

        # filter out stopwords from t_corpus
        st_corpus = [[w for w in t_txt if w not in stoplist] for t_txt in t_corpus]  # stop_word_token_corpus

        # # grams
        # ct_ngrams = set((g[1], g[0]) for g in bigram_ct.export_phrases(t_corpus))
        # ct_ngrams = sorted(list(ct_ngrams))
        # print(len(ct_ngrams), "grams with common terms found")
        # # highest scores
        # print(ct_ngrams[-20:])

        # Count word frequencies
        from collections import defaultdict
        frequency = defaultdict(int)
        for text in st_corpus:
            for token in text:
                frequency[token] += 1

        # Only keep words that appear more than once
        processed_corpus = [[token for token in text if frequency[token] > 1] for text in st_corpus]
        dictionary = corpora.Dictionary(processed_corpus)
        bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
        tfidf = models.TfidfModel(bow_corpus)
        self.id_to_score_corpus = tfidf[bow_corpus] # bpbpbp: vector
        self.processed_corpus = processed_corpus # bpbpbp:tokens

if __name__=="__main__":
    import pprint
    pprinter = pprint.PrettyPrinter().pprint

    #get file path
    pdf_file = pdf_extractor.get_pdf_file_in_texts("reinforcement-an-introduction.pdf")

    #preprocess pdf into text-> corpus, pages, headers
    analyzer = TopicAnalyzer(pdf_file)

    print(analyzer)
