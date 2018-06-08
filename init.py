import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import subprocess
import timeit

# write a function to return neighbours
def main(size, return_plot, run_ms):
    # currently starts out with empty grid
    # in the future if random positions are populated it will be included
    class Model(object):
        prob = 0.5
        timeout = 0

        def __init__(self, size):
            self.size = size
            self.space = np.zeros([size for i in range(3)], dtype='int')
            self.active_grid = []
            self.pointx = []
            self.pointy = []
            self.pointz = []
            self.xstate = []
            self.ystate = []
            self.zstate = []
            self.monitor = []
            self.level = []
            self.counter = 0
            # for poisson processes
            self.timestamp = []
            self.migration_param = []

        @staticmethod
        def populate_nbs(position):
            neighbour = ([[position[0] + 1, position[1], position[2]],
                          [position[0] - 1, position[1], position[2]],
                          [position[0], position[1] + 1, position[2]],
                          [position[0], position[1] - 1, position[2]],
                          [position[0], position[1], position[2] + 1],
                          [position[0], position[1], position[2] - 1]])
            return neighbour

        def flat_pos(self,pos):
            if pos != None:
                return str(pos[0]+self.size*(pos[1]+self.size*pos[2]))

        def vaccant_nbs(self, position):
            # position is a list of length 3
            # this function should only return empty neighbours
            vaccant_deems = []
            for locations in self.populate_nbs(position):
                if max(locations) == size or min(locations) < 0:
                    continue
                if self.space[tuple(locations)] == 0:
                    vaccant_deems.append(locations)
            return vaccant_deems

        def grid_chooser(self, position):
            vaccant_sites = self.vaccant_nbs(position)
            if len(vaccant_sites) > 0:
                return vaccant_sites[np.random.randint(len(vaccant_sites))]

        def pop_mig(self, met_site):
            self.space[tuple(met_site)] = 1
            self.active_grid.append(met_site)
            self.pointx.append([met_site[0]])
            self.pointy.append([met_site[1]])
            self.pointz.append([met_site[2]])
            self.xstate = []
            self.ystate = []
            self.zstate = []

            while len(self.active_grid) > 0:
                for sites in self.active_grid:
                    #if len(self.vaccant_nbs(sites)) > 0:
                    if np.random.random() < self.prob:
                        continue
                    choice = self.grid_chooser(sites)
                    if choice != None:
                        self.migration_param.append('-m')
                        self.migration_param.append(self.flat_pos(sites))
                        self.migration_param.append(self.flat_pos(choice))
                    if choice is not None and self.space[tuple(choice)] == 0:
                        self.space[tuple(choice)] = 1
                        if choice not in self.active_grid:
                            self.active_grid.append(choice)
                            self.active_grid = [sites for sites in self.active_grid if len(self.vaccant_nbs(sites)) > 0]
                            self.xstate.append(choice[0])
                            self.ystate.append(choice[1])
                            self.zstate.append(choice[2])
                            continue
                self.pointx.append(self.xstate)
                self.pointy.append(self.ystate)
                self.pointz.append(self.zstate)
                self.xstate = []
                self.ystate = []
                self.zstate = []


        def poisson_migration(self, position, depth=0):
            self.level.append(depth)
            if len(self.timestamp) <= depth:
                self.timestamp.append(0)
            while len(self.vaccant_nbs(position)) > 0:
                # for i in range(10):
                choice = self.grid_chooser(position)
                interval = np.random.exponential(self.prob)
                print(self.timestamp)
                print(len(self.timestamp))
                if choice is None:
                    return 0
                if self.space[tuple(choice)] == 0:
                    if interval >= self.timestamp[depth]:
                        self.timestamp[depth] += interval
                        self.space[tuple(choice)] = 1
                        self.pointx.append(choice[0])
                        self.pointy.append(choice[1])
                        self.pointz.append(choice[2])
                        if np.sum(self.space) < (size ** 3 - 1):
                            self.poisson_migration(choice, depth=depth + 1)
                    else:
                        if self.timeout < 1000:
                            self.timeout += 1
                        else:
                            return 0
                else:
                    self.poisson_migration(choice, depth=depth + 1)

    grid = Model(size)
    position = [np.random.randint(size) for i in range(3)]
    grid.pop_mig(position)

    if run_ms is True:
        node_pop = 15
        total_sample = str(node_pop*size**3)
        ms_defaults = ['ms',total_sample, '1', 'T', '-t', '1', '-I', str(size**3)]
        layout = ['0' for i in range(size**3)]
        layout[0] = total_sample
        ms_defaults = ms_defaults + layout + grid.migration_param
        print(ms_defaults)
        print('\n Time for size of grid {} \t'.format(size))
        print(timeit.timeit(subprocess.call(' '.join(ms_defaults)),number=100, shell=True))

    # grid.space[tuple(position)] = 1
    # Creating the Animation object
    # grid.poisson_migration(position)

    def upgrade_iterator(num):
        return ax.scatter(grid.pointx[num],
                          grid.pointy[num],
                          grid.pointz[num],
                          s=50, marker='*', c='orange')

    def update(num):
        return ax.scatter(([grid.pointx[i] for i in index_sets[num][:, 0]]),
                          ([grid.pointy[i] for i in index_sets[num][:, 0]]),
                          ([grid.pointz[i] for i in index_sets[num][:, 0]]),
                          s=50, marker='*', c='orange')

    if return_plot == ('yes' or 'y'):
        fig = plt.figure()
        ax = p3.Axes3D(fig)
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_zlim(0, size)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        animate = animation.FuncAnimation(fig, upgrade_iterator, frames=len(grid.pointx),interval = 120)
        animate.save('animate.mp4', writer = 'ffmpeg')
        plt.show()

if __name__ == '__main__':
    for i in range(10):
        main(i+3,'n',True)
