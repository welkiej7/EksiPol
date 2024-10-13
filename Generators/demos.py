import igraph as ig
import warnings 
import numpy as np 
from user_space_generators import generate_user_space_gaussian, generate_user_space_mixed, generate_user_space_polarized, generate_user_space_uniform_discrete
from network_generators import NETWORK_GENERATOR_POL
import seaborn as sns
import matplotlib.pyplot as plt 



def heatmaps_p_np_30():
    POL = NETWORK_GENERATOR_POL(generate_user_space_mixed(30,n_non_polarized_topics=0,n_polarized_topics=1,n_normal_topics=0))
    NPOL = NETWORK_GENERATOR_POL(generate_user_space_gaussian(30, 0.34, 3, 3))

    sns.heatmap(POL.calculate_similarity(), cmap = 'viridis')
    plt.title('Polarized, Lower the Score Less the Similarity')
    plt.show()
    sns.heatmap(NPOL.calculate_similarity(), cmap= 'viridis')
    plt.title('Non Polarized, Lower the Score Less the Similarity ')
    plt.show()


