from random import random

class Particle():
    '''
        asd
    '''
    def __init__(self, limits, value = 1e20, coord = None):
        '''
            asd
        '''
		if coord is None:
			coord = [uniform(lb, ub) for lb, ub in limits]
		velo = [uniform(ub-lb, lb-ub)]
        self.coord = coord
        self.velo = velo
        self.value = value
        self.best_coord = coord
        self.best_value = value

    def __repr__(self):
        '''
            aasd
        '''
        string = 'Particle ({0:< 10.2f}): {1:< 10.2f}\t'+str(self.coord)
        return string.format(self.best_value, self.value)

    def next(self, best_swarm, omega, fi_p, fi_s):
        '''
            asd
        '''
        v_p = [random() for _ in self.coord]
        v_s = [random() for _ in self.coord]
        self.velo = [omega*self.velo[i] + fi_p*v_p[i]*(self.best_coord[i] - c) + \
                     fi_s*v_s[i]*(best_swarm[i] - c) for i, c in enumerate(self.coord)]
        self.coord = [c + self.velo[i] for i, c in enumerate(self.coord)]

    def update(self):
        '''
            asd
        '''
        if self.value < self.best_value:
            self.best_value = self.value
            self.best_coord = self.coord

			
class Swarm(list):
	def __init__(self, func, limits, generate = True, num_particles = 100, particles = None):
		self.best_coord = []
		self.best_value = 1e20
		self.func = func
		if generate:
			for _ in range(num_particles):
				self.append(Particle(limits))
			self.solve()
			self.update()
		else:
			for value, coord in particles:
				self.append(Particle(limits, value, coord))
			self.update()
	
	def __repr__(self):
		string = 'Swarm:\n'
		for p in self:
			string += '\t'+str(p) + '\n'
		return string
	
	def update(self):
		for p in self:
			p.update()
			if self.best_value > p.value:
				self.best_value = p.value
				self.best_coord = p.coord
	
	def solve(self):
		for p in self:
			p.value = self.func(p.coord)
	
	def next(self, omega, fi_p, fi_s):
		for p in self:
			p.next(self.best_coord, omega, fi_p, fi_s)
	
def pso(func, lb, ub, generate = True, num_particles = 100, particles = None, continue_ = False, path_to_swarm = None):
	if  continue_:
		with open(path_to_swarm, 'rb') as f:
			S = pickle.load(f)
	else:
		assert len(lb) == len(ub), 'Lower-bound and upper-bound must be the same length.'
		limits = zip(lb, ub)
		assert all(l_b < u_b for l_b, u_b in limits), 'All lower-bounds must be less then upper-bounds.'
		if generate:
			S = Swarm(func, limits, generate, num_particles)
		else:
			assert particles is None, 'Input particles, or set generate to True'
			S = Swarm(func, limits, generate, particles)
	while True:
		prev = S.best_value
		S.next()
		S.solve()
		S.update()
		curr = S.best_value
		if abs(curr-prev) <= eps:
			return S.best_value, S.best_coord