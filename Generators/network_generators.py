import igraph as ig
import warnings 
import numpy as np 
from user_space_generators import generate_user_space_gaussian, generate_user_space_mixed, generate_user_space_polarized, generate_user_space_uniform_discrete
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import sys
from PIL import Image
import os 

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
    
    def generate_a_retweet_network(self, TOPIC_NO:int, ECHO_CHAMBER_STRENGTH:float, AVG_RETWEET:float = 1, SD_RETWEET:float = 0.5, HPOW:float = 100):
        '''
        Generates a retweet network from an already existing network embedded in the graph. The number of retweet a user makes
        is sampled either from a normal distribution or a power law distribution. 

        @param ECHO_CHAMBER_STRENGTH:float Probability of a user retweeting from her follower list.
        @param HASHTAG_PROB:float Probability of a user retweeting from any user that is similar to her.
        @param AVG_RETWEET: If using a normal distribution, average number of retweet a user will make.
        @param SD_RETWEET: If using a normal distribution, standard deviation of the distribution.
        '''


        if not hasattr(self, 'network'):
            raise AttributeError(f'Object does not contain a graph embedded:\n{self}')
        


        # Find the number of retweets per user. 

        EXPECTED_RETWEET_COUNT = np.round(np.random.normal(AVG_RETWEET, SD_RETWEET, size = self.user_similarity_matrix.shape[0]))
        HASHTAG_PROB = 1 - ECHO_CHAMBER_STRENGTH
        EDGE_LIST = []
        for USER in tqdm(range(self.user_similarity_matrix.shape[0]), desc = 'Retweeting...'):
            TMP_RETWEET_COUNT = EXPECTED_RETWEET_COUNT[USER]
            for RETWEET in range(int(TMP_RETWEET_COUNT)):
                OBSERVATION = np.random.choice(['F','H'], size = int(TMP_RETWEET_COUNT), replace = True, p = [ECHO_CHAMBER_STRENGTH,HASHTAG_PROB])
                for CAST in OBSERVATION:
                    if CAST == 'H':
                        RETWEET_CANDIDATES = list(self.user_space[:,TOPIC_NO])
                        RETWEET_CANDIDATES = 1 - abs(RETWEET_CANDIDATES - RETWEET_CANDIDATES[USER])

                        RETWEET_CANDIDATES[USER] = 0 # Prevent self loops
                        RETWEET_CANDIDATES = [0 if i<0 else i for i in RETWEET_CANDIDATES]
                        RETWEET_CANDIDATES = [0.99 if i == 1 else i for i in RETWEET_CANDIDATES]
                        
            
                        CAST = np.random.choice(RETWEET_CANDIDATES, size = 1, p = (np.array(RETWEET_CANDIDATES)**HPOW) / np.sum(np.array(RETWEET_CANDIDATES)**HPOW))
                        CASTED_NODE = np.where(np.array(RETWEET_CANDIDATES) == CAST)[0]
                        if len(CASTED_NODE) == 0:
                            continue
                        else:
                            EDGE_LIST.append((USER,CASTED_NODE[0]))
                    if CAST == 'F':
                        RETWEET_CANDIDATES = self.network.neighborhood(USER)

                        CASTED_NODE = np.random.choice(RETWEET_CANDIDATES, size = 1, replace = False)
                        EDGE_LIST.append((USER,CASTED_NODE.item()))
    
        self.retweet_network = ig.Graph(self.user_similarity_matrix.shape[0], EDGE_LIST, directed = True).simplify(loops = True)



    def PLOT(self,TOPIC_NO, layout = 'kk'):

        colormap = plt.cm.viridis
        vertex_colors = [colormap(value) for value in self.user_space[:,TOPIC_NO]]
        vertex_colors_hex = [mcolors.to_hex(color) for color in vertex_colors]
        self.network.vs['color'] = vertex_colors_hex
        self.network.vs["label"] = [i for i in range(self.network.vcount())]
        self.layout = self.network.layout_kamada_kawai()

    def GIF_IT(self, TOPIC_NO, OUTPUT_FILE_NAME, original_network = True):
        if original_network:
            EDGE_LIST = self.network.get_edgelist()
        else:
            EDGE_LIST = self.retweet_network.get_edgelist()
        os.system('mkdir GIF')
        
        for _ in range(len(EDGE_LIST)):
            GRAPH = ig.Graph(self.user_similarity_matrix.shape[0], EDGE_LIST[0:_])
            colormap = plt.cm.viridis
            vertex_colors = [colormap(value) for value in self.user_space[:,TOPIC_NO]]
            vertex_colors_hex = [mcolors.to_hex(color) for color in vertex_colors]
            self.network.vs['color'] = vertex_colors_hex
            self.network.vs["label"] = [i for i in range(self.network.vcount())]
            self.layout = self.network.layout_kamada_kawai()
            

            ig.plot(GRAPH, vertex_color = self.network.vs['color'], vertex_label = self.network.vs["label"], layout = self.layout, target= f"GIF/{_}.png")
            last = _
        
        if _ == len(EDGE_LIST) - 1:
            for TOPIC in range(self.user_space.shape[1]):
                colormap = plt.cm.magma
                vertex_colors = [colormap(value) for value in self.user_space[:,TOPIC]]
                vertex_colors_hex = [mcolors.to_hex(color) for color in vertex_colors]
                self.network.vs['color'] = vertex_colors_hex
                self.network.vs["label"] = [i for i in range(self.network.vcount())]
                ig.plot(GRAPH, vertex_color = self.network.vs['color'], vertex_label = self.network.vs["label"], layout = self.layout, target= f"GIF/{last + TOPIC}.png")


        FRAMES = [f"GIF/{_}.png" for _ in range(len(EDGE_LIST) + self.user_space.shape[1] - 1)]
        GIF_FRAMES = []
        for i in FRAMES:
            GIF_FRAMES.append(Image.open(i))

        GIF_FRAMES[0].save(OUTPUT_FILE_NAME, save_all = True, append_images = GIF_FRAMES[0:], duration = 100, loop = 0)
        
        os.system('rm -r GIF')

    def CALCULATE_SEPERATION(self,TOPIC):
        return np.mean([abs(self.user_space[x,TOPIC] - self.user_space[y,TOPIC]) for (x,y) in self.retweet_network.get_edgelist()])