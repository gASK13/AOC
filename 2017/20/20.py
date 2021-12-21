import common


class Particle:
    def __init__(self, line):
        # p = < -460, 662, -3843 >, v = < -21, -20, -165 >, a = < 2, 0, 16 >
        self.position = [int(p) for p in line.split('>')[0].split('p=<')[1].split(',')]
        self.velocity = [int(p) for p in line.split('>')[1].split('v=<')[1].split(',')]
        self.acceleration = [int(p) for p in line.split('>')[2].split('a=<')[1].split(',')]

    def sum_acc(self):
        return sum([abs(a) for a in self.acceleration])

    def sum_vc(self):
        return sum([abs(v) for v in self.velocity])

    def tick(self):
        self.velocity = [self.velocity[i] + self.acceleration[i] for i in range(3)]
        self.position = [self.velocity[i] + self.position[i] for i in range(3)]

    def __key(self):
        return self.position[0], self.position[1], self.position[2]

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Particle):
            return self.__key() == other.__key()
        return NotImplemented


def get_closest(particles):
    min_acc = 9999999
    for i in range(len(particles)):
        a = particles[i].sum_acc()
        if a < min_acc:
            min_acc = a

    min_vel = 9999999
    min_idx = 0
    for i in range(len(particles)):
        if particles[i].sum_acc() == min_acc:
            if particles[i].sum_vc() < min_vel:
                min_idx = i
                min_vel = particles[i].sum_vc()
    return min_idx


def simulate(particles):
    for i in range(1000):
        collisions = {}
        for p in particles:
            if p not in collisions:
                collisions[p] = []
            collisions[p].append(p)

        for c in collisions:
            if len(collisions[c]) > 1:
                for p in collisions[c]:
                    particles.remove(p)
        for p in particles:
            p.tick()
    return particles


print(f'PT #1 {get_closest(common.Loader.transform_lines(Particle))}')
print(f'PT #2 {len(simulate(common.Loader.transform_lines(Particle)))}')

# PT 2
#   tick -> move -> check (hash?)
#