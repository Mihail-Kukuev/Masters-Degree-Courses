import argparse
import math
import pickle
from collections import Counter, defaultdict
from operator import itemgetter

from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

import string

from numpy import mean

LEMMATIZER = WordNetLemmatizer()
STEMMER = SnowballStemmer('english', True)
UNWANTED_WORDS = set(stopwords.words('english')) | set(string.punctuation)


class InvertedIndexData:
    def __init__(self, inv_indexes, doc_lengths):
        self.inv_indexes = inv_indexes
        self.doc_lengths = doc_lengths
        self.mean_doc_length = mean(doc_lengths.values())

    def doc_len(self, doc_id):
        return self.doc_lengths[doc_id]

    def mean_doc_len(self):
        return self.mean_doc_length

    def tf(self, term, doc_id):
        if self.inv_indexes.get(term, None) and self.inv_indexes[term].get(doc_id, None):
            return self.inv_indexes[term][doc_id]
        else:
            return 0

    def df(self, term):
        return len(self.inv_indexes.get(term, {}))

    def relevant_docs(self, term):
        return self.inv_indexes.get(term, {}).keys()

    def docs_amount(self):
        return len(self.doc_lengths)

    def dict_size(self):
        return len(self.inv_indexes)

    def mean_word_pos_len(self):
        return mean([len(docs) for docs in self.inv_indexes.values()])

    def max_word_pos_len(self):
        return max(len(docs) for docs in self.inv_indexes.values())


class Document:
    def __init__(self, id=0):
        self.id = id
        self.title = ""
        self.annotation = ""


class Query:
    def __init__(self, id=0):
        self.id = id
        self.text = ""
        self.words = []


def run_with_cmd():
    parser = argparse.ArgumentParser(add_help=True)
    subparsers = parser.add_subparsers(dest='command', help='List of commands')

    index_parser = subparsers.add_parser('index', help=
    'Takes an input file with texts, builds an inverted index and saves it in binary format')
    index_parser.add_argument('texts_file', help='Input file with texts')

    search_parser = subparsers.add_parser('search', help=
    'Loads the inverted index into memory, takes a file with queries and outputs search result to another file')
    search_parser.add_argument('queries_file', help='Input file with queries')
    search_parser.add_argument('answer_file', help='Output file for search results')
    search_parser.add_argument('-k1', '--k1', type=float, default=1.2, help='k1 coefficient')
    search_parser.add_argument('-b', '--b', type=float, default=0.75, help='k1 coefficient')
    search_parser.add_argument('-k2', '--k2', type=float, default=0, help='k2 coefficient')

    args = parser.parse_args()

    if args.command == 'index':
        create_save_index(args.texts_file)
    elif args.command == 'search':
        search(args.queries_file, args.answer_file, args.k1, args.b, args.k2)
    else:
        print('Error. Not enough arguments.')


def create_save_index(data_filename):
    docs = load_documents(data_filename)
    inv_index_data = create_inverted_index(docs, title_only=False)
    print_statistics(inv_index_data)

    dump_file = open(dump_filename, 'wb')
    pickle.dump(inv_index_data, dump_file)
    dump_file.close()
    print('Index was created and saved in \"%s\".' % dump_filename)


dump_filename = 'index.bin'


def search(queries_filename, answer_filename, k1, b, k2):
    queries = load_queries(queries_filename)
    for query in queries:
        query.words = normalize(query.text)

    dump_file = open(dump_filename, 'rb')
    inv_index = pickle.load(dump_file)
    dump_file.close()

    with open(answer_filename, 'w') as output_file:
        for query in queries:
            for relevant_doc_id in bm25_search(query, inv_index, k1, b, k2):
                output_file.write('%d %d\n' % (query.id, relevant_doc_id))

    print('Search results are saved in \"%s\".' % answer_filename)


def bm25_search(query, inv_index_data, k1, b, k2):
    relevant_docs = set()
    for word in set(query.words):
        relevant_docs.update(inv_index_data.relevant_docs(word))
    doc_rsv_lst = [(doc_id, rsv(query, doc_id, inv_index_data, k1, b, k2))
                   for doc_id in relevant_docs]
    sorted_doc_rsv = sorted(doc_rsv_lst, key=itemgetter(1), reverse=True)
    # return [doc_id for doc_id, doc_rsv in sorted_doc_rsv[:10] if doc_rsv > 10]
    return [doc_id for doc_id, doc_rsv in sorted_doc_rsv[:10]]


def rsv(query, doc_id, inv_index_data, k1, b, k2):
    L = float(inv_index_data.doc_len(doc_id))
    L_mean = float(inv_index_data.mean_doc_len())
    N = inv_index_data.docs_amount()
    res = 0.0
    tfq_dict = Counter(query.words)
    # idf_sum = 0.0
    for word in set(query.words):
        tf = inv_index_data.tf(word, doc_id)
        df = inv_index_data.df(word)
        idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
        tfq = tfq_dict[word]
        # idf_sum += idf
        res += idf * tf * (k1 + 1) / (k1 * (1 - b + b * L / L_mean) + tf) * (k2 + 1) * tfq / (k2 + tfq)
    return res


def print_statistics(inv_index_data):
    print("Dictionary size: %d" % inv_index_data.dict_size())
    print("Mean document length: %d" % inv_index_data.mean_doc_len())
    print("Mean word positions length: %f" % inv_index_data.mean_word_pos_len())
    print("Max word positions length: %d" % inv_index_data.max_word_pos_len())


def create_inverted_index(documents, title_only=False):
    doc_lengths = {}
    inv_indexes = defaultdict(dict)

    for doc in documents:
        text = doc.title if title_only else doc.annotation
        words = normalize(text)

        doc_lengths[doc.id] = len(words)

        for word, freq in Counter(words).iteritems():
            inv_indexes[word][doc.id] = freq

    return InvertedIndexData(inv_indexes, doc_lengths)


def normalize(text):
    tokens = word_tokenize(text.lower())
    strip_symbols = '0123456789/'
    lemmas = [STEMMER.stem(token).strip(strip_symbols) for token in tokens]
    # lemmas = [LEMMATIZER.lemmatize(token).strip(strip_symbols) for token in tokens]
    return [w for w in lemmas if w not in UNWANTED_WORDS and len(w) > 0]


def load_queries(filename):
    queries = list()
    id_counter = 1
    with open(filename, 'r') as input_file:
        line = input_file.readline()
        while line.strip():
            if line.startswith(".I"):
                query = Query(id_counter)
                id_counter += 1
                line = input_file.readline()
            elif line.startswith(".W"):
                line = input_file.readline()
                while (not line.startswith(".I")) and line.strip():
                    query.text += line
                    line = input_file.readline()
                queries.append(query)
            else:
                line = input_file.readline()

    return queries


def load_documents(filename):
    docs = list()
    with open(filename, 'r') as input_file:
        line = input_file.readline()
        while line.strip():
            if line.startswith(".I"):
                doc = Document()
                doc.id = int(line[3:])
                line = input_file.readline()
            elif line.startswith(".T"):
                line = input_file.readline()
                while not line.startswith(".A"):
                    doc.title += line
                    line = input_file.readline()
            elif line.startswith(".W"):
                line = input_file.readline()
                while (not line.startswith(".I")) and line.strip():
                    doc.annotation += line
                    line = input_file.readline()
                docs.append(doc)
            else:
                line = input_file.readline()
    return docs


run_with_cmd()
