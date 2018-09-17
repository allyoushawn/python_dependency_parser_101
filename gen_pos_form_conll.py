import pdb

conll = 'en_ewt-ud-train.conll'
op_f = open('op.pos', 'w')
with open(conll) as f:
    for line in f.readlines():
        if line.rstrip() == '':
            op_f.write('\n')
            continue
        tokens = line.rstrip().split('\t')
        if len(tokens) < 1:
            pdb.set_trace()
        wrd = tokens[1]
        tag = tokens[3]
        op_f.write('{}/{} '.format(wrd, tag))
op_f.close()
