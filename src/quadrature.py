import itertools



QUADS = ['R', 'I']

def all_(num_dims):
    """
    Int -> [[Q]]
    """
    return itertools.product(*([QUADS] * num_dims))

def one_random(num_dims, seed=None):
    """
    Int -> Maybe Int -> [Q]
    """
    choices = list(all_(num_dims))
    if seed is not None: random.seed(seed)
    return choices[random.randint(0, len(choices) - 1)]

def all_reals(num_dims):
    """
    Int -> [Q]
    """
    return ['R'] * num_dims

def first_random_second_both(seed=None):
    """
    Maybe Int -> [[Q]]
    """
    if seed is not None: random.seed(seed)
    first = QUADS[random.randint(0, 1)]
    return [[first, 'R'], [first, 'I']]

