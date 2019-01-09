from operator import itemgetter

import networkx as nx
import pickle

from crawl import WikiPage


def calculate_ranks():
    dump_file = open('wiki_pages.bin', 'rb')
    pages_dict = pickle.load(dump_file)
    dump_file.close()

    graph = create_graph(pages_dict)

    pagerank(graph, 0.85, pages_dict)
    pagerank(graph, 0.95, pages_dict)
    pagerank(graph, 0.5, pages_dict)
    pagerank(graph, 0.3, pages_dict)

    hits(graph, pages_dict)


def create_graph(pages_dict):
    graph = nx.DiGraph()
    for url, page in pages_dict.iteritems():
        for link in page.links:
            if link in pages_dict:
                graph.add_edge(url, link)
    return graph


def pagerank(graph, alpha, pages_dict):
    pageranks = nx.pagerank(graph, alpha=alpha)
    top10_ranks = top10(pageranks, pages_dict)

    print_pages_results(top10_ranks, 'PageRank results, alpha=%s' % alpha)


def hits(graph, pages_dict):
    hubs, authorities = nx.hits(graph, max_iter=500, tol=0.1)

    mean_hits = {}
    for url, hub in hubs.iteritems():
        mean_hits[url] = (hub + authorities[url]) / 2.0

    top10_hubs = top10(hubs, pages_dict)
    top10_authorities = top10(authorities, pages_dict)
    top10_mean_hits = top10(mean_hits, pages_dict)

    print_pages_results(top10_hubs, 'Hubs results')
    print_pages_results(top10_authorities, 'Authorities results')
    print_pages_results     (top10_mean_hits, 'Mean hits results')


def top10(items_dict, pages_dict):
    ranks = sorted(items_dict.iteritems(), key=itemgetter(1), reverse=True)[:10]
    return [(pages_dict[url], rank) for url, rank in ranks]


def print_pages_results(pages_results, title=""):
    print('\n%s:' % title)
    print '--------------------------------------------------------'
    for page, rank in pages_results:
        print('{}  < {} >'.format(page.title, rank))
        print(page.url)
        print('%s\n' % page.snippet)


calculate_ranks()
