import numpy as np
from sklearn.metrics import ndcg_score
from sklearn.metrics import precision_score
from sklearn.metrics import average_precision_score

def parse_qrel_line(qrel_line):
    split = qrel_line.split()
    qid = split[0]
    docid = split[2]
    relevancy = split[3]
    return qid, docid, relevancy

def parse_result_line(result_line):
    split = result_line.split()
    qid = split[0]
    docid = split[1]
    rank = split[2]
    score = split[3]

    return qid, docid, rank, score


def relevancy_lookup(qrel_text):
    with open(qrel_text, 'r') as answers:
        relevancies = {}
        for line in answers:
            qid, docid, relevancy = parse_qrel_line(line)

            if qid not in relevancies:
                relevancies[qid] = {docid:relevancy}
            else:
                relevancies[qid].update({docid:relevancy})
    return relevancies
