import matplotlib.pyplot as plt
import scipy.misc
from scipy import ndimage
import numpy as np


class SimpleOccupancyMap():

    def __init__(self, path):
        self._map = plt.imread(path)[:, :, 0]
        self._map = ndimage.rotate( self._map, -90)
        self._freespace = np.argwhere(self._map > 0.5)

        self.sampling_counter = 0
        self.map_access_counter = 0
    def show(self):
        plt.imshow(self._map.transpose(1,0), origin='lower', cmap="gray")

    def sample_state(self):
        self.sampling_counter+=1
        return np.floor(np.random.uniform([0, 0], self._map.shape)).astype(np.int)

    def sample_valid_state(self):
        self.sampling_counter += 1
        ix = int(np.random.uniform(0, len(self._freespace)))
        return self._freespace[ix, :]

    def is_occupied(self,x,y):
        self.map_access_counter += 1
        return self._map[int(x),int(y)] < 0.5

    def reset_counters(self):
        self.map_access_counter = 0
        self.sampling_counter = 0

    def print_statistics(self):
        print("Samplings " + str(self.sampling_counter))
        print("Map Access " + str(self.map_access_counter))

if __name__ == "__main__":
    occ_map = SimpleOccupancyMap("/tmp/test.png")
    occ_map.show()
    plt.show()
    all_samples = np.array([occ_map.sample_state() for x in range(0,10000)])
    valid_samples = np.array([occ_map.sample_valid_state() for x in range(0, 100000)])

    plt.scatter(*all_samples.T, marker='.')
    plt.scatter(*valid_samples.T, marker='.')
    plt.show()

    print(occ_map.is_occupied(200,200))
