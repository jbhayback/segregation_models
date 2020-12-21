import random
import numpy as np

# Class that handles Schelling Agent attributes and methods
class Schelling:
    
    def __init__(self, input_data, similarity_threshold, neighbors_count):
        self.similarity_threshold = similarity_threshold
        self.neighbors_count = neighbors_count
        self.data_grid = input_data.values
    
    def run_simulation(self):
        # Runs the Schelling's segragation model simulation for one iteration.
        for (row, col), value in np.ndenumerate(self.data_grid):
            char_type = self.data_grid[row, col]
            if char_type != 0:
                neighborhood = self.data_grid[row-self.neighbors_count:row+self.neighbors_count, col-self.neighbors_count:col+self.neighbors_count]
                neighborhood_size = np.size(neighborhood)
                empty_cells_count = len(np.where(neighborhood == 0)[0])

                if neighborhood_size != empty_cells_count + 1:
                    similar_chars = len(np.where(neighborhood == char_type)[0]) - 1
                    similarity_ratio = similar_chars / (neighborhood_size - empty_cells_count - 1.)

                    # Char is unsatisfied if its similarity ratio is lower than the similarity threshold
                    is_unsatisfied = (similarity_ratio < self.similarity_threshold)
                    if is_unsatisfied:
                        empty_cells = list(zip(np.where(self.data_grid == 0)[0], np.where(self.data_grid == 0)[1]))
                        
                        # The unsatisfied char type will randomly move to empty cell in the grid and its previous location will now become empty
                        random_empty_cell = random.choice(empty_cells)
                        self.data_grid[random_empty_cell] = char_type
                        self.data_grid[row,col] = 0

    def get_average_similarity_ratio(self):
        # Calculates the average similarity ratio across all agents for the entire data grid
        count = 0
        similarity_ratio = 0
        for (row, col), value in np.ndenumerate(self.data_grid):
            char_type = self.data_grid[row, col]
            if char_type != 0:
                neighborhood = self.data_grid[row-self.neighbors_count:row+self.neighbors_count, col-self.neighbors_count:col+self.neighbors_count]
                neighborhood_size = np.size(neighborhood)
                empty_cells_count = len(np.where(neighborhood == 0)[0])
                if neighborhood_size != empty_cells_count + 1:
                    similar_chars = len(np.where(neighborhood == char_type)[0]) - 1
                    similarity_ratio += similar_chars / (neighborhood_size - empty_cells_count - 1.)
                    count += 1

        return similarity_ratio / count
