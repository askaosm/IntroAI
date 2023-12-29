import numpy as np


def joint_distribution_of_word_counts(texts, word0, word1):
    """
    Parameters:
    texts (list of lists) - a list of texts; each text is a list of words
    word0 (str) - the first word to count
    word1 (str) - the second word to count

    Output:
    Pjoint (numpy array) - Pjoint[m,n] = P(X0=m,X1=n), where
      X0 is the number of times that word0 occurs in a given text,
      X1 is the number of times that word1 occurs in the same text.
    """
    #init #joint의 크기를 결정하기 위해 
    max_count_word0= 0
    max_count_word1=0


    #find the maximum number of occurences 
    for text in texts:
      count_word0=text.count(word0)
      count_word1=text.count(word1)
      
      
      if count_word0> max_count_word0:
          max_count_word0=count_word0 #update max count word
      if count_word1 > max_count_word1:
          max_count_word1=count_word1

    #create zero joint  -> return jpint
    Pjoint=np.zeros((max_count_word0+1, max_count_word1+1))  #
      
      #calculate the Joint distribution 
    for text in texts:
        count_word0=text.count(word0)
        count_word1=text.count(word1)
        Pjoint[count_word0, count_word1] +=1
      
    Pjoint/=np.sum(Pjoint)
    #raise RuntimeError("You need to write this part!")
    return Pjoint


def marginal_distribution_of_word_counts(Pjoint, index):
    """
    Parameters:
    Pjoint (numpy array) - Pjoint[m,n] = P(X0=m,X1=n), where
      X0 is the number of times that word0 occurs in a given text,
      X1 is the number of times that word1 occurs in the same text.
    index (0 or 1) - which variable to retain (marginalize the other)

    Output:
    Pmarginal (numpy array) - Pmarginal[x] = P(X=x), where
      if index==0, then X is X0
      if index==1, then X is X1
    """
    Pmarginal = np.sum(Pjoint,axis=1-index)
    return Pmarginal


def conditional_distribution_of_word_counts(Pjoint, Pmarginal):
    """
    Parameters:
    Pjoint (numpy array) - Pjoint[m,n] = P(X0=m,X1=n), where
      X0 is the number of times that word0 occurs in a given text,
      X1 is the number of times that word1 occurs in the same text.
    Pmarginal (numpy array) - Pmarginal[m] = P(X0=m)

    Outputs:
    Pcond (numpy array) - Pcond[m,n] = P(X1=n|X0=m)
    """
    #init
    Pcond= np.zeros_like(Pjoint)
    #calculate the conditional probability
    for m in range(Pjoint.shape[0]):
        if Pmarginal[m] > 0:
            Pcond[m, :] = Pjoint[m, :] / Pmarginal[m]
        else:
            Pcond[m, :] = np.nan  

  
    return Pcond


def mean_from_distribution(P):
    """
    Parameters:
    P (numpy array) - P[n] = P(X=n)

    Outputs:
    mu (float) - the mean of X
    """
    values = np.arange(len(P))
    mu = np.sum(values * P)
    #mu = np.floor(mu * 1000) / 1000
    mu = np.round(mu, 3)
    return mu


def variance_from_distribution(P):
    """
    Parameters:
    P (numpy array) - P[n] = P(X=n)

    Outputs:
    var (float) - the variance of X
    """
    # calculate the mean
    values = np.arange(len(P))
    mu = np.sum(values * P)

    #calculate variance
    var=np.sum(((values-mu)**2)*P)
    #var = np.floor(var * 1000) / 1000
    var = np.round(var, 3)
    return var


def covariance_from_distribution(P):
    """
    Parameters:
    P (numpy array) - P[m,n] = P(X0=m,X1=n)

    Outputs:
    covar (float) - the covariance of X0 and X1
    """
    #calculate the mean of X0 and X1
    x0_values = np.arange(P.shape[0])
    x1_values = np.arange(P.shape[1])
    mu_X0 = np.sum(x0_values * np.sum(P, axis=1))
    mu_X1 = np.sum(x1_values * np.sum(P, axis=0))

    M, N = np.meshgrid(x0_values, x1_values, indexing='ij')

    # Calculate the covariance
    covar = np.sum((M - mu_X0) * (N - mu_X1) * P)
    #covar = np.floor(covar * 1000) / 1000
    covar = np.round(covar, 3)

    
    return covar



def expectation_of_a_function(P, f):
    """
    Parameters:
    P (numpy array) - joint distribution, P[m,n] = P(X0=m,X1=n)
    f (function) - f should be a function that takes two
       real-valued inputs, x0 and x1.  The output, z=f(x0,x1),
       must be a real number for all values of (x0,x1)
       such that P(X0=x0,X1=x1) is nonzero.

    Output:
    expected (float) - the expected value, E[f(X0,X1)]
    """
    
    x0_values = np.arange(P.shape[0])
    x1_values = np.arange(P.shape[1])
    M, N = np.meshgrid(x0_values, x1_values, indexing='ij')
    
    # Calculate the expected value
    expected = np.sum(f(M, N) * P)
    #expected = np.floor(expected * 1000) / 1000
    expected= np.round(expected, 3)
    return expected
    