import json


class Node:
    def __init__(self, dict_data: dict, node_number, next_numbers: list, prev=None):
        self.prev = prev
        self.node_number = node_number
        self.next_numbers = next_numbers.copy()
        self.next_numbers.remove(node_number)
        if prev is None:
            self.c = 0
            self.value = 0
        else:
            self.c = prev.c
            self.value = prev.value
        self.c += dict_data['D'][node_number]
        if dict_data['I'][node_number] > self.c:
            self.value += (dict_data['I'][node_number] - self.c) * dict_data['a'][node_number]
        else:
            self.value += (self.c - dict_data['I'][node_number]) * dict_data['b'][node_number]

    def __repr__(self):
        temp = self
        res = ''
        while temp:
            res = ' -> {} ({})'.format(temp.node_number, temp.value) + res
            temp = temp.prev
        res = 'start' + res
        return res


def display_table(d: dict):
    n = len(d['I'])
    print('   ', end='')
    for i in range(n):
        print('{: >6}'.format(i), end='')
    print()
    for k in d.keys():
        print('  ' + k, end='')
        for i in d[k]:
            print('{: >6}'.format(i), end='')
        print()


# def check_route(node: Node, maybe_min, maybe_max: Node, trash):
#     if node.next_numbers:
#         if maybe_max.value <= node.value:
#             trash.append(node)
#         else:
#             maybe_min.append(node)
#     elif maybe_max.value > node.value:
#         trash.append(maybe_max)
#         maybe_max = node
#         for i in maybe_min.copy():
#             if i.value >= maybe_max.value:
#                 maybe_min.remove(i)
#                 trash.append(i)
#     else:
#         trash.append(node)
#     return maybe_min, maybe_max, trash

def check_route2(node: Node, maybe_min, maybe_max: Node):
    if node.next_numbers:
        if maybe_max.value > node.value:
            maybe_min.append(node)
    elif maybe_max.value > node.value:
        maybe_max = node
        for i in maybe_min:
            if i.value >= maybe_max.value:
                maybe_min.remove(i)
    return maybe_min, maybe_max


def find_min_route(data, maybe_min, maybe_max: Node, trash=None, k=0):
    if trash is None:
        trash = []
    while True:
        if not maybe_min:
            return {
                'top route': maybe_max.__str__(),
                # 'trash': trash,
                'iter': k
            }
        min_value = min(maybe_min, key=lambda x: x.value)
        maybe_min.remove(min_value)
        if min_value.value >= maybe_max.value:
            del min_value
            continue

        for i in min_value.next_numbers:
            node = Node(data, i, min_value.next_numbers, min_value)
            k += 1
            if len(node.next_numbers) == 1:
                node = Node(data, node.next_numbers[0], node.next_numbers, node)
                k += 1
            # maybe_min, maybe_max, trash = check_route(node, maybe_min, maybe_max, trash)
            # maybe_min, maybe_max = check_route2(node, maybe_min, maybe_max)
            if node.next_numbers:
                if maybe_max.value > node.value:
                    maybe_min.append(node)
            elif maybe_max.value > node.value:
                maybe_max = node



def find(data: dict):
    k = 0
    maybe_min = []
    n = len(data['I'])
    for i in range(n):
        node = Node(data, i, list(range(n)))
        k += 1
        maybe_min.append(node)
    node = maybe_min.pop(0)
    for i in range(1, n):
        node = Node(data, i, node.next_numbers, node)
        k += 1
    maybe_max = node
    return find_min_route(data, maybe_min, maybe_max)


if __name__ == '__main__':
    d: dict
    with open('input.json', 'r') as f:
        d = json.load(f)
    display_table(d)
    a = find(d)
    print(a['top route'])
    # trash = sorted(a['trash'], key=lambda x: x.value)
    # print(trash)
    # for i in trash:
    #     print(i)
