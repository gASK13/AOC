def hash_list(_list, delimiter='#'):
    return delimiter.join([str(x) for x in _list])

def transpose_matrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]