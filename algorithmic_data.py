import random

def generate(operations, samples, max_list_len=4, max_operand = 9, stop_token='.'):
    data = []
    for _ in range(samples):
        list_len = random.randint(2, max_list_len)
        op = random.choice(operations)
        # generate a random list of numbers
        x = [random.randint(0, max_operand) for _ in range(list_len)]
        
        # apply the operation to the list
        result = op(x)
        
        token_sequence = f'{op.__name__}{x}={result}{stop_token}'
        # strip the white space
        token_sequence = token_sequence.replace(' ', '')
        data.append(token_sequence)
    return data


def generate_comp(operations, samples, max_list_len=3, max_operand = 9, stop_token='.'):
    data = []
    for _ in range(samples):
        list_len1 = random.randint(2, max_list_len)
        list_len2 = random.randint(2, max_list_len)
        op1 = random.choice(operations)
        op2 = random.choice(operations)
        op3 = random.choice(operations)
        # generate a random list of numbers
        x1 = [random.randint(0, max_operand) for _ in range(list_len1)]
        x2 = [random.randint(0, max_operand) for _ in range(list_len2)]
        # apply the operation to the list
        res1 = op1(x1)
        res2 = op2(x2)

        if not isinstance(res1, list):
            res1 = [res1]
        if not isinstance(res2, list):
            res2 = [res2]
        result = op3(res1 + res2)
        token_sequence = f'{op3.__name__}[{op1.__name__}{x1},{op2.__name__}{x2}]={result}{stop_token}'
        # strip the white space
        token_sequence = token_sequence.replace(' ', '')
        data.append(token_sequence)
    return data

def generate_tree(operations, recurse_prob, max_child, values):
    """
    @param operations a list of operations that we can apply to lists of tokens
    @param recurse_prob the probability of recursing (creating a subtree)
    @param max_child the maximum number of child nodes for each node.
    @param values a set of values that can be sampled at leaf nodes.

    @return a dictionary representing a tree, with the following keys:
    - result: the result of the operation
    - data: a string representing the tree

    @note we assume that each operation works on lists of values, e.g.,
    `sum([1, 2, 3])` returns `6`. the 6 should be wrapped inside of a list, too,
    `[6]`, so that operations can be composed as we move up the tree.
    the final output may be a single value, in which case we will remove the
    list wrapper.

    @note the leaf values should make sense in the context of the operations.
    they should also be serializable as bytes to be used in the n-gram model.
    an operation should produce output that also makes sense in the context of
    the operations and the n-gram model.

    @note we also augment each node with a description of what the operation is
    doing to the data, so that we can generate a human-readable description of
    process of evaluating the expression, which may be useful as training data
    for larger AR models (process supervision).
    """
    if random.random() < recurse_prob:
        num_nodes = random.randint(1, max_child)
        op = random.choice(operations)
        childs = [generate_tree(operations, recurse_prob, max_child, values) for _ in range(num_nodes)]
        result = op([child['result'] for child in childs])
        data = f'{op.__name__}[{",".join([child["data"] for child in childs])}]'
        return {'result': result, 'data': data}
    else:
        return {'result': random.choice(values), 'data': str(random.choice(values))}


