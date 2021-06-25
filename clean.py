"""
    This program merges different pages of threads in
    The Magic Cafe Dataset
"""
import sys
import json
import re


def main():
    """ Main function of the program """
    dataset = {}
    lookup = set()
    with open(sys.argv[1]) as input_file:
        for row in input_file:
            data = json.loads(row)
            forum_id = re.findall(r"forum=([0-9]+)", data['link'])
            topic_id = re.findall(r"topic=([0-9]+)", data['link'])
            start = re.findall(r"start=([0-9]+)", data['link'])
            start = ''.join(start)
            if len(forum_id) == 0:
                forum_id = ['-1']

            # key = forum_id[0] + '_' + topic_id[0]
            key = topic_id[0]
            if key not in dataset:
                dataset[key] = [data]
                lookup.add(key+'_'+start)
            elif 'page' in data and key+'_'+start not in lookup:
                dataset[key].append(data)
                lookup.add(key+'_'+start)

    for key, value in dataset.items():
        if len(value) > 1:
            sort_list = sorted(value, key=lambda i: int(i['page']))
            new_list = sort_list[0]
            for posts in sort_list[1:]:
                new_list['posts'] += posts['posts']
            new_list['total_pages'] = len(sort_list)
            print(json.dumps(new_list))
        else:
            print(json.dumps(value[0]))
        sys.stdout.flush()


if __name__ == '__main__':
    main()
