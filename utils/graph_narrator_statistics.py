# avoid the error: maximum recursion depth exceeded in comparison
import sys
import resource
sys.setrecursionlimit(3000)  
max_rec = 0x100000
resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
sys.setrecursionlimit(max_rec)

import numpy as np
from collections import Counter, defaultdict
import unidecode
from rouge import Rouge
rouge = Rouge()

def get_nodes(n):
    n = n.strip()
    n = n.replace('(', '')
    n = n.replace('\"', '')
    n = n.replace(')', '')
    n = n.replace(',', ' ')
    n = n.replace('_', ' ')
    n = n.replace('-', ' ')
    n = n.replace('/', ' ')
    n = unidecode.unidecode(n)
    #n = n.lower()
    return n

def get_relation(edge_label):
    edges_combined = edge_label.split('-')
    new_edge_label = ''
    if len(edges_combined) == 2:
        edge0 = edges_combined[0]
        edge1 = edges_combined[1]
        pos_label_0 = edge0.index("/", edge0.index("/")+1) + 1
        pos_label_1 = edge1.index("/", edge1.index("/")+1) + 1
        new_edge_label = edge0[pos_label_0:] + '  ' + edge1[pos_label_1:]
        new_edge_label = new_edge_label.replace('/', ' ')
        new_edge_label = new_edge_label.replace('-', ' ')
        new_edge_label = new_edge_label.replace('_', ' ')
    elif len(edges_combined) == 1:
        edge0 = edges_combined[0]
        if "/" in edge0:
            pos_label_0 = edge0.index("/", edge0.index("/")+1) + 1
            new_edge_label = edge0[pos_label_0:]
            new_edge_label = new_edge_label.replace('/', ' ')
            new_edge_label = new_edge_label.replace('-', ' ')
            new_edge_label = new_edge_label.replace('_', ' ')
        else:
            new_edge_label = edge0
    return new_edge_label

def compute_rouge_score(s1, s2):
    """ compute the rouge score between two sentences
    """
    scores = rouge.get_scores(s1, s2)
    return scores[0]['rouge-1']['f']

def read_data(path):
    data = np.load(path, allow_pickle=True)
    data = data.tolist()
    return data

def get_statistic(data):
    cnt = {}
    for triple_num, domains in data.items():
        sm_token = 0
        sm_str = 0
        instance_cnt = 0
        for _, instances in domains.items():
            for instance in instances:
                sm_token += len(instance['sdp_sentence'].split())
                sm_str += len(instance['sdp_sentence'])
                instance_cnt += 1
        cnt[triple_num] = [sm_token/instance_cnt, sm_str/instance_cnt]
    return cnt

def filter_by_rouge_threshold(data, threshold):
    cnt = defaultdict(lambda: [0, 0])
    instance_cnt = 0
    for triple_num, domains in data.items():
        for domain, instances in domains.items():
            for i, instance in enumerate(instances):
                xml_triples = instance['xml_triples']
                sentence_text = instance['sentence_text']
                sdp_sentence = instance['sdp_sentence']
                triple_tokens = []
                for triple in xml_triples:
                    triple = triple.split(' | ')
                    entity1 = get_nodes(triple[0])
                    entity2 = get_nodes(triple[2])
                    relation = get_relation(triple[1])
                    triple_tokens.append(' '.join([entity1, relation, entity2]))
                triple_tokens = ''.join(triple_tokens)
                origin_rouge_score = compute_rouge_score(sentence_text, triple_tokens)
                sdp_rouge_score = compute_rouge_score(sdp_sentence, triple_tokens)
                cnt[triple_num][0] += (origin_rouge_score >= threshold)
                cnt[triple_num][1] += (sdp_rouge_score >= threshold)
                data[triple_num][domain][i]['origin_rouge_above_'+str(threshold)] = (origin_rouge_score >= threshold)
                data[triple_num][domain][i]['sdp_rouge_above_'+str(threshold)] = (sdp_rouge_score >= threshold)
                instance_cnt += 1
                if instance_cnt%100000==0:
                    print('Processed instances: ', instance_cnt, cnt)
    cnt['all'] = [instance_cnt, sum(v[0] for k, v in cnt.items()), sum(v[1] for k, v in cnt.items())]
    return cnt, data


if __name__ == '__main__':
    ##### read data from npy format ####
    dev_data = read_data('./dataset_complete/npy_format_dataset_complete/dev.npy')
    test_data = read_data('./dataset_complete/npy_format_dataset_complete/test.npy')
    train_data = read_data('./dataset_complete/npy_format_dataset_complete/train.npy')

    #### get statistic ####
    # dev_cnt = get_statistic(dev_data)
    # test_cnt = get_statistic(test_data)
    # train_cnt = get_statistic(train_data)
    # print("Dev statistic: ", dev_cnt)
    # print("Test statistic: ", test_cnt)
    # print("Train statistic: ", train_cnt)

    #### filter by rouge score ####
    threshold = 0.8
    dev_cnt, dev_data_with_rouge = filter_by_rouge_threshold(dev_data, threshold=threshold)
    np.save('./dataset_complete/npy_format_dataset_complete/dev_with_rouge_'+str(threshold)+'.npy', dev_data_with_rouge)
    test_cnt, test_data_with_rouge = filter_by_rouge_threshold(test_data, threshold=threshold)
    np.save('./dataset_complete/npy_format_dataset_complete/test_with_rouge_'+str(threshold)+'.npy', test_data_with_rouge)
    train_cnt, train_data_with_rouge = filter_by_rouge_threshold(train_data, threshold=threshold)
    np.save('./dataset_complete/npy_format_dataset_complete/train_with_rouge_'+str(threshold)+'.npy', train_data_with_rouge)

    print("Dev statistic: ", dev_cnt)
    print("Test statistic: ", test_cnt)
    print("Train statistic: ", train_cnt)