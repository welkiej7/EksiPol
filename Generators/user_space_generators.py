import numpy as np 
import warnings


def generate_user_space_uniform_discrete(n_users:int,
                                n_opinion_dimension:int=2,
                                n_values:int=3):
    '''
    Definition: Generates a user opinion space. Matrix with n_users rows and opinion_dimension_n
    columns. Hence OP = ||_{n_users * opinion_dimension}. Then assigns n possible values between -1 and 1
    to the cells. Values are taken from a uniform distribution.

    @param n_users:int = Number of Users
    @param n_opinion_dimension:int = Number of possible opinions or subjects.
    @param n_values:int = Number of possible values that an opinion can take.
    '''
    values = np.linspace(-1,1,n_values)
    picked_values = np.random.choice(values, size = n_users * n_opinion_dimension)
    user_matrix = picked_values.reshape((n_users, n_opinion_dimension))

    return user_matrix

def generate_aligned_user_space_uniform(n_users:int, n_opinion_dimension:int, alignment_strength:str = 'high'):
    
    '''
    Definition: Generates an aligned user space from a uniform distribution.

    @param n_users:int Number of users
    @param n_opinion_dimension:int Number of opinions
    @param alignment_strength:(high,moderate,low) The alignment strength of the topics.
    '''
    
    if alignment_strength == 'high':
        RETURN_MATRIX = np.zeros(shape = (n_users, n_opinion_dimension))
        core_values = np.random.uniform(-1,1,size = n_users)
        RETURN_MATRIX[:,0] = core_values
        for _ in range(1,n_opinion_dimension):
            TMP_values = []
            for k in core_values:
                TMP_values.append(np.random.normal(k, scale = 0.05, size = 1)[0])
                [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in TMP_values]
            TMP_values = np.array(TMP_values)
            RETURN_MATRIX[:,_] = TMP_values

    elif alignment_strength == 'moderate':

        RETURN_MATRIX = np.zeros(shape = (n_users, n_opinion_dimension))
        core_values = np.random.uniform(-1,1,size = n_users)
        RETURN_MATRIX[:,0] = core_values
        for _ in range(1,n_opinion_dimension):
            TMP_values = []
            for k in core_values:
                TMP_values.append(np.random.normal(k, scale = 0.15, size = 1)[0])
                [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in TMP_values]
            TMP_values = np.array(TMP_values)
            RETURN_MATRIX[:,_] = TMP_values
    elif alignment_strength == 'low':

        RETURN_MATRIX = np.zeros(shape = (n_users, n_opinion_dimension))
        core_values = np.random.uniform(-1,1,size = n_users)
        RETURN_MATRIX[:,0] = core_values
        for _ in range(1,n_opinion_dimension):
            TMP_values = []
            for k in core_values:
                TMP_values.append(np.random.normal(k, scale = 0.25, size = 1)[0])
                TMP_values = [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in TMP_values]
            TMP_values = np.array(TMP_values)
            RETURN_MATRIX[:,_] = TMP_values

    else:
        raise ValueError('Undefined value string for the alignment strength')
    



    return RETURN_MATRIX

def generate_user_space_gaussian(n_users:int, 
                                 sd:float, 
                                 n_opinion_dimension:int = 2, 
                                 n_values:int = 3):
    '''
    Definition: Generates a user opinion space. Matrix with n_users rows and opinion_dimension_n
    columns. Hence OP = ||_{n_users * opinion_dimension}. Then assigns n possible values between -1 and 1
    to the cells. Values are taken from a gaussian distribution. The mean of the distribution is always zero
    scale of the distribution can be changed.

    @param n_users:int = Number of Users
    @param n_opinion_dimension:int = Number of possible opinions or subjects.
    @param n_values:int = Number of possible values that an opinion can take.
    @param sd:float = The standart deviation of the gaussian distribution.
    '''
    if sd > 0.35:
        warnings.warn('Generated distribution might sample from outside of the opinion space. These values will be ignored.')
    values = np.random.normal(loc = 0, scale = sd, size = n_users * n_opinion_dimension)
    values = np.array([i if (i > -1 and i < 1) else -888 for i in values])
    values = np.delete(values, np.where(values == -888)[0])
    user_matrix = np.zeros(shape = (n_users,n_opinion_dimension))

    for index in range(n_opinion_dimension):
        picked_values = np.random.choice(values, size = n_users)
        user_matrix[:,index] = picked_values
    
    
    return user_matrix

def generate_aligned_user_space_gaussian(n_users:int, 
                                 sd:float, 
                                 n_opinion_dimension:int = 2, 
                                 alignment_strength:str = 'high'):
    
    if sd > 0.35:
        warnings.warn('Generated distribution might sample from outside of the opinion space. These values will be ignored and returned to their max value.')
    
    core_values = list(np.random.normal(loc = 0, scale = sd, size = n_users))
    core_values = [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in core_values]

    if alignment_strength == 'high':
        RETURN_MATRIX = np.zeros(shape = (n_users, n_opinion_dimension))
        RETURN_MATRIX[:,0] = core_values
        for _ in range(1,n_opinion_dimension):
            TMP_values = []
            for k in core_values:
                TMP_values.append(np.random.normal(k, scale = .03, size = 1)[0])
                [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in TMP_values]
            TMP_values = np.array(TMP_values)
            RETURN_MATRIX[:,_] = TMP_values

    elif alignment_strength == 'moderate':

        RETURN_MATRIX = np.zeros(shape = (n_users, n_opinion_dimension))
        core_values = np.random.uniform(-1,1,size = n_users)
        RETURN_MATRIX[:,0] = core_values
        for _ in range(1,n_opinion_dimension):
            TMP_values = []
            for k in core_values:
                TMP_values.append(np.random.normal(k, scale = .9, size = 1)[0])
                [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in TMP_values]
            TMP_values = np.array(TMP_values)
            RETURN_MATRIX[:,_] = TMP_values

    elif alignment_strength == 'low':

        RETURN_MATRIX = np.zeros(shape = (n_users, n_opinion_dimension))
        core_values = np.random.uniform(-1,1,size = n_users)
        RETURN_MATRIX[:,0] = core_values
        for _ in range(1,n_opinion_dimension):
            TMP_values = []
            for k in core_values:
                TMP_values.append(np.random.normal(k, scale = .2 , size = 1)[0])
                TMP_values = [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in TMP_values]
            TMP_values = np.array(TMP_values)
            RETURN_MATRIX[:,_] = TMP_values

    else:
        raise ValueError('Undefined value string for the alignment strength')

    return RETURN_MATRIX



def generate_user_space_polarized(n_users:int, n_opinion_dimension, alpha, beta):
    
    '''
    Definition: Generates a user opinion space. Matrix with n_users rows and opinion_dimension_n
    columns. Hence OP = ||_{n_users * opinion_dimension}. Then assigns n possible values between -1 and 1
    to the cells. Values are taken from a beta distribution and then scaled to fit between -1 and 1. 

    @param n_users:int = Number of Users
    @param n_opinion_dimension:int = Number of possible opinions or subjects.
    @param alpha:float = alpha value of a beta distribution.
    @param beta:float = beta value of a beta distribution.

    '''
    
    user_matrix = np.zeros(shape = (n_users,n_opinion_dimension))
    for index in range(n_opinion_dimension):
        values = np.random.beta(alpha,beta,n_users)
        user_matrix[:,index] = [(i - 0.5) * 2 for i in values]
    
    return user_matrix



def generate_aligned_user_space_polarized(n_users:int, n_opinion_dimension:int, alpha:float, beta:float, alignment_strength:float):
    RETURN_MATRIX = np.zeros(shape = (n_users,n_opinion_dimension))
    core_values = np.random.beta(alpha,beta,n_users)
    RETURN_MATRIX[:,0] = core_values
    for _ in range(1,n_opinion_dimension):
        TMP_values = []
        for k in core_values:
            TMP_values.append(np.random.normal(k, scale = alignment_strength , size = 1)[0])
            TMP_values = [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in TMP_values]
        TMP_values = np.array(TMP_values)
        RETURN_MATRIX[:,_] = TMP_values

    return RETURN_MATRIX



def generate_user_space_mixed(n_users,
                               n_non_polarized_topics,
                               n_polarized_topics,
                               n_normal_topics):

    '''
    Definition: Generates a user opinion space as a matrix with n_users rows and total topic count columns.
    Hence OP = ||_{n_users * (n_non_polarized_topics + n_polarized_topics + n_normal_topics)}. Then assigns
    values between -1 and 1 to the cells according to their properties. Generated user space matrix
    always have the non polarized topics at first, then polarized topics then normal topics.  
    
    @param n_users:int = Number of Users
    @param n_non_polarized_topics:int = Number of non polarized topics
    @param n_polarized_topics:int = Number of polarized topics
    @param n_normal_topics:int = Number of normal topics. 
    '''


    user_matrix = np.zeros(shape=(n_users, n_non_polarized_topics + n_polarized_topics + n_normal_topics))
    for _ in range(n_non_polarized_topics):
        values = np.random.normal(loc = 0, scale = .35, size = n_users)
        user_matrix[:,_] = values

    for _ in range(n_non_polarized_topics, n_non_polarized_topics + n_polarized_topics):
        values = np.random.beta(0.5,0.5,n_users)
        values = [(i - 0.5) * 2 for i in values]
        user_matrix[:,_] = values
    
    for _ in range(n_non_polarized_topics + n_polarized_topics, n_non_polarized_topics + n_polarized_topics + n_normal_topics):
        user_matrix[:,_] = np.random.uniform(0,1,n_users)


    return user_matrix


def generate_aligned_user_space_mixed(n_users:int,
                                      n_non_polarized_topics:int,
                                      n_polarized_topics:int,
                                      n_normal_topics:int,
                                      alignment_strength:float):
    

    RETURN_MATRIX = np.zeros(shape=(n_users, n_non_polarized_topics + n_polarized_topics + n_normal_topics))
    core_values = np.random.normal(loc = 0, scale = .3, size = n_users)
    RETURN_MATRIX[:,0] = core_values
    
    for _ in range(1,n_non_polarized_topics):
        TMP_values = []
        for k in core_values:
            TMP_values.append(np.random.normal(k, scale = alignment_strength , size = 1)[0])
            TMP_values = [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in TMP_values]
        TMP_values = np.array(TMP_values)
        RETURN_MATRIX[:,_] = TMP_values
    
    core_values = np.random.beta(0.5,0.5,n_users)

    for _ in range(n_non_polarized_topics, n_non_polarized_topics + n_polarized_topics):
        TMP_values = []
        for k in core_values:
            TMP_values.append(np.random.normal(k, scale = alignment_strength , size = 1)[0])
            TMP_values = [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in TMP_values]
        TMP_values = np.array(TMP_values)
        RETURN_MATRIX[:,_] = TMP_values

    core_values = np.random.uniform(-1,1,size = n_users)
    for _ in range(n_non_polarized_topics + n_polarized_topics, n_non_polarized_topics + n_polarized_topics + n_normal_topics):
        TMP_values = []
        for k in core_values:
            TMP_values.append(np.random.normal(k, scale = alignment_strength , size = 1)[0])
            TMP_values = [i if (i > -1) and (i<1) else -1 if i < -1 else 1 for i in TMP_values]
        TMP_values = np.array(TMP_values)
        RETURN_MATRIX[:,_] = TMP_values
    

    return RETURN_MATRIX



