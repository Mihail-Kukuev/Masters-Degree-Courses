import subprocess
from collections import defaultdict
from operator import itemgetter

import numpy

groundtruth_file = 'qrel_clean'
answer_file = 'answer'


def k2_pick_up():
    k2_values = numpy.arange(0, 1000, 100)
    k1 = 1.81
    b = 0.78

    results = [max_func_k2(k2) for k2 in k2_values]
    for k2, score in sorted(results, key=itemgetter(1), reverse=True)[:10]:
        print 'k2=%f, MAP@10=%f' % (k2, score)


def max_func_k2(k2):
    subprocess.call(['python', './inv_index.py', 'search', 'cran.qry', 'answer', '-k1', str(1.81), '-b', str(0.78), '-k2', str(k2)])
    q2retrd = read_search_results()
    return k2, map10(q2retrd)


def grid_search():
    k1_values = numpy.arange(1.6, 2, 0.01)
    b_values = numpy.arange(0.7, 0.8, 0.01)
    k2 = 0

    results = [max_func_k1_b(k1, b) for k1 in k1_values for b in b_values]
    for k1, b, score in sorted(results, key=itemgetter(2), reverse=True)[:10]:
        print 'k1=%f, b=%f, MAP@10=%f' % (k1, b, score)


def max_func_k1_b(k1, b):
    subprocess.call(['python', './inv_index.py', 'search', 'cran.qry', 'answer', '-k1', str(k1), '-b', str(b)])
    q2retrd = read_search_results()
    return k1, b, map10(q2retrd)


def read_search_results():
    q2retrd = defaultdict(list)
    for line in open(answer_file):
        qid, did = [int(x) for x in line.split()]
        q2retrd[qid].append(did)
    return q2retrd


def map10(q2retrd):
    N = len(q2retrd.keys())
    MAP = 0.0
    for q in q2retrd.keys():
        n_results = min(10, len(q2retrd[q]))
        avep = numpy.zeros(n_results)
        for i in range(n_results):
            avep[i:] += q2retrd[q][i] in q2reld[q]
            avep[i] *= (q2retrd[q][i] in q2reld[q]) / (i + 1.0)
        MAP += sum(avep) / min(n_results, len(q2reld[q]))
    return MAP / N


q2reld = defaultdict(set)
for line in open(groundtruth_file):
    qid, did = [int(x) for x in line.split()]
    q2reld[qid].add(did)

grid_search()
# k2_pick_up()
