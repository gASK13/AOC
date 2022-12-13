import common
import hashlib

class Hasher:
    def __init__(self):
        self._cache = {}

    def hash(self, text, hash_count):
        for i in range(hash_count):
            if text in self._cache:
                text = self._cache[text]
            else:
                hsh = hashlib.md5(text.encode('utf-8')).hexdigest()
                self._cache[text] = hsh
                text = hsh
        return text


def find_quintuplet(hash):
    quints = []
    for i in range(len(hash) - 4):
        if hash[i] == hash[i+1] == hash[i+2] == hash[i+3] == hash[i+4]:
            quints.append(hash[i])
    return quints


def find_triplet(hash):
    for i in range(len(hash) - 2):
        if hash[i] == hash[i + 1] == hash[i + 2]:
            return [hash[i]]
    return []

def get_pads(salt, hash_count=1, limit=64):
    pads = []
    idx = 0
    triplets = {}
    queue = []
    hasher = Hasher()
    while len(pads) < limit:
        hsh = hasher.hash(f'{salt}{idx}', hash_count)
        for quintuplet in find_quintuplet(hsh):
            if quintuplet in triplets:
                queue += [ix for ix in triplets[quintuplet] if idx <= ix + 1000]
                triplets[quintuplet] = []
        for triplet in find_triplet(hsh):
            if triplet not in triplets:
                triplets[triplet] = []
            triplets[triplet].append(idx)
        queue.sort()
        while len(queue) > 0 and queue[0] + 1000 < idx:
            pads.append(queue.pop(0))
        idx += 1
    return pads


assert get_pads('abc', limit=1) == [39]
assert get_pads('abc', limit=2) == [39, 92]
assert get_pads('abc')[-1] == 22728

print(f'So the 64th pad is at index {get_pads(common.Loader.load_lines()[0])[-1]}')

assert get_pads('abc', hash_count=2017, limit=1) == [10]
assert get_pads('abc', hash_count=2017)[-1] == 22551

print(f'So the 2017th 64th pad is at index {get_pads(common.Loader.load_lines()[0], hash_count=2017)[-1]}')