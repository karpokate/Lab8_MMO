from main import find
import time
import json
from random import randint


def test_data(d: dict, n, min_value, max_value):
    res = d.copy()
    for k in res.keys():
        for i in range(n):
            res[k].append(randint(min_value, max_value))
    return res


def display_table_file(d: dict, f):
    n = len(d['I'])
    f.write('   ')
    for i in range(n):
        f.write('{: >6}'.format(i))
    f.write('\n')
    for k in d.keys():
        f.write('  ' + k)
        for i in d[k]:
            f.write('{: >6}'.format(i))
        f.write('\n')


if __name__ == '__main__':
    d = {}

    for i in range(10, 21):
        for j in range(1):
            print('start({}, {})'.format(i,j))
            with open('test.json', 'r') as f:
                d = json.load(f)
            test = test_data(d, i, 0, 20)
            with open('test ' + str(i) + '_' + str(j) + '.txt', 'w') as f:
                display_table_file(test, f)
                n = len(d['I'])
                ful_iter = 1
                for i in range(1, n + 1):
                    ful_iter = i * ful_iter + 1
                ful_iter -= 1
                f.write('Max iter: ' + str(ful_iter) + '\n')
                print(ful_iter)
                t=time.time()
                res = find(test)
                t2=time.time()-t
                f.write('iter: ' + str(res['iter']) + '\n')
                f.write('top route: ' + res['top route'] + '\n')
                f.write('time: {}s.\n'.format(t2))
            print('finish({}, {})'.format(i,j))
