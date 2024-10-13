import igraph as ig
import warnings 
import numpy as np 
from user_space_generators import generate_user_space_gaussian, generate_user_space_mixed, generate_user_space_polarized, generate_user_space_uniform_discrete
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class SEQ_GENERATOR():
    
    def __init__(self, user_space) -> None:
        self.user_space = user_space    
    
    def __repr__(self) -> str:
        
        return f'Network Generator at {hex(id(self))}'

    def accept_deg_dist(self,deg_dist:list):
        
        if len(deg_dist) != self.user_space.shape[0]:
            raise ValueError('Offered degree distribution list does not have the same length with the user space provided.')
        
        self.deg_dist = deg_dist
    
    def calculate_similarity(self, method:str = 'euc', normalize = True):
        '''
        Method can be dot product or euclidean distance. If normalize is True, the similarity will be given between 0 and 1.
        '''
        self.user_similarity_matrix = np.zeros(shape = (self.user_space.shape[0], 
                                                        self.user_space.shape[0]))
        if method not in ['euc','dot']:
            raise ValueError('Method must be Euclidean: euc or Dot Product: dot')
        if method == 'euc':
            for USER_MAIN in range(self.user_space.shape[0]):
                for CONNECTION_MAIN in range(USER_MAIN, self.user_space.shape[0]):
                    self.user_similarity_matrix[USER_MAIN,CONNECTION_MAIN] = np.linalg.norm(self.user_space[USER_MAIN] - self.user_space[CONNECTION_MAIN])
        else:
            for USER_MAIN in range(self.user_space.shape[0]):
                for CONNECTION_MAIN in range(USER_MAIN, self.user_space.shape[0]):
                    self.user_similarity_matrix[USER_MAIN,CONNECTION_MAIN] = self.user_space[USER_MAIN]@self.user_space[CONNECTION_MAIN]


        
        self.user_similarity_matrix = self.user_similarity_matrix + self.user_similarity_matrix.T - np.diag(self.user_similarity_matrix.diagonal())
        if normalize:
            self.user_similarity_matrix = np.max(self.user_similarity_matrix) - self.user_similarity_matrix
            self.user_similarity_matrix = (self.user_similarity_matrix - np.min(self.user_similarity_matrix)) / (np.max(self.user_similarity_matrix) - np.min(self.user_similarity_matrix))
        
        return self.user_similarity_matrix
    
    def connect_sequential(self, HPOW, observe_all = True):

        '''
        Definition: Nodes start connecting sequentially according to the degree that they own and the
        homophily degree. If homophily is -absolute- nodes will always prefer the highest similarity
        and if the similarity is the same, they will pick one randomly. If homophily is --strong-- they will 
        connect to one of the top round √n/2 users randomly. If homophily is --mediocre-- they will connect to 
        top 2√n users randomly. If homophily is --low-- they will connect to top 4√n users randomly and finally
        if homophily is --none-- they will connect randomly.
        
        '''
        if not hasattr(self,'deg_dist'):
            raise AttributeError('Network generator object does not have a degree distribution.')
        
        if not hasattr(self, 'user_similarity_matrix'):
            raise AttributeError('Network generator object does not have a user similarity matrix.')

        # Randomly assign the degrees from the degree distribution to the nodes. 
        if observe_all:
            self.node_degrees = np.random.choice(self.deg_dist, size = self.user_space.shape[0])
            EDGES = []
            for NODE in tqdm(range(self.user_similarity_matrix.shape[0]), desc = 'Casting Votes...'):
                CANDIDATES = self.user_similarity_matrix[NODE]
                CANDIDATES[NODE] = 0
                CANDIDATES = (CANDIDATES**HPOW) / np.sum(CANDIDATES**HPOW)
                TOT_CAST = self.node_degrees[NODE]
                
                conns = np.random.choice(range(len(CANDIDATES)), size = TOT_CAST, replace = False, p = CANDIDATES)
                for _ in conns:
                    EDGES.append((NODE,_))

            self.network = ig.Graph(len(self.user_similarity_matrix[NODE]), EDGES, directed = False).simplify(multiple = True)
        
    def PLOT(self,TOPIC_NO):

        colormap = plt.cm.viridis
        vertex_colors = [colormap(value) for value in self.user_space[:,TOPIC_NO]]
        vertex_colors_hex = [mcolors.to_hex(color) for color in vertex_colors]
        self.network.vs['color'] = vertex_colors_hex
        self.network.vs["label"] = [i for i in range(self.network.vcount())]
        self.layout = self.network.layout_kamada_kawai()
