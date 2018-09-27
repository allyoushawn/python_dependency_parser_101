#!/usr/bin/env python3

from nltk.parse.stanford import StanfordDependencyParser
import sys
import pdb
import time
import pickle

path_to_jar = '../nltk_stanford/stanford-parser-full-2018-02-27/stanford-parser.jar'
path_to_models_jar = '../nltk_stanford/stanford-english-corenlp-2018-02-27-models.jar'
heldout_in ='data/en_ewt-ud-dev.pos'
heldout_gold = 'data/en_ewt-ud-dev.conll'

class DefaultList(list):
    """A list that returns a default value if index out of bounds."""
    def __init__(self, default=None):
        self.default = default
        list.__init__(self)

    def __getitem__(self, index):
        try:
            return list.__getitem__(self, index)
        except IndexError:
            return self.default
def pad_tokens(tokens):
    tokens.insert(0, '<start>')
    tokens.append('ROOT')

# We use the function to read input sentences
def read_pos(loc):
    for line in open(loc):
        if not line.strip():
            continue
        words = DefaultList('')
        tags = DefaultList('')
        for token in line.split():
            if not token:
                continue
            word, tag = token.rsplit('/', 1)
            #words.append(normalize(word))
            words.append(word)
            tags.append(tag)
        pad_tokens(words); pad_tokens(tags)
        yield words, tags


# The function reads a conllx file which contains all information about sentences
# including wrd, pos, heads and labels.
def read_conll(loc):
    for sent_str in open(loc).read().strip().split('\n\n'):
        lines = [line.split() for line in sent_str.split('\n')]
        words = DefaultList(''); tags = DefaultList('')
        heads = [None]; labels = [None]
        for i, line in enumerate(lines):
            word = line[2]
            pos = line[3]
            head = line[6]
            label = line[7]
            words.append(sys.intern(word))
            #words.append(intern(normalize(word)))
            tags.append(sys.intern(pos))
            heads.append(int(head) if head != '0' else len(lines) + 1)
            labels.append(label)
        pad_tokens(words); pad_tokens(tags)
        yield words, tags, heads, labels


def get_root_distance(current_node, gold_heads):
    dist = 0
    head = current_node
    while True:
        if head == 0:
            break
        head = gold_heads[head]
        dist += 1
    return dist




dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
result = dependency_parser.raw_parse('I shot an elephant in my pants with another elephant   ')

dep = next(result)
#print(list(dep.triples()))
tmp = dep.nodes[2]['head']


# input_sents is a list of tuples.
# Each tuple contains two elements, (wrd, pos) with type (str, str)
input_sents = list(read_pos(heldout_in))
# sentences is a list of tuples.
# Each tuple contains two elements, (wrd, pos, head, label) with type (str, str, int, str)
gold_sents = list(read_conll(heldout_gold))

c = 0
t = 0
t1 = time.time()
counter = 0
hit = [0] * 12
total = [0] * 12

print('Total sentence to be evaluated: {}'.format(len(input_sents)))
for (words, tags), (_, _, gold_heads, gold_labels) in zip(input_sents, gold_sents):
    counter += 1
    if counter % 10 == 0:
        print('Evaluating sentence {}'.format(counter))
    feed = ''
    for i in range(len(words)):
        if i == 0: continue
        if i == len(words) - 1: break
        feed = feed + words[i] + ' '
    result = dependency_parser.raw_parse(feed)
    dep = next(result)
    # Add a dummy element
    heads = [-1] * (len(words))
    for i in dep.nodes.keys():
            try:
                try:
                    wrd_idx = words.index(dep.nodes[i]['word'])
                except:
                    continue
                heads[wrd_idx] = dep.nodes[i]['head']
            except:
                pdb.set_trace()

    modified_gold_heads = [1]
    for i in range(len(gold_labels)):
        if i == 0: continue
        if gold_heads[i] == len(gold_heads):
            modified_gold_heads.append(0)
        else:
            modified_gold_heads.append(gold_heads[i])

    for i, w in list(enumerate(words))[1:-1]:
        if gold_labels[i] in ('P', 'punct'):
            continue
        dist = get_root_distance(i, modified_gold_heads)
        try:
            if heads[i] == modified_gold_heads[i]:
                c += 1
                if dist <= 10:
                    hit[dist] += 1
                else:
                    hit[11] += 1
        except:
            pdb.set_trace()
        t += 1
        if dist <= 10:
            total[dist] += 1
        else:
            total[11] += 1

with open('stanford_hit.pkl', 'wb') as fp:
    pickle.dump(hit, fp)
with open('stanford_total.pkl', 'wb') as fp:
    pickle.dump(total, fp)

t2 = time.time()
print('Parsing took %0.3f ms' % ((t2-t1)*1000.0))
print('{} {} {:.4f}'.format(c, t, float(c)/t))
