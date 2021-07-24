"""
A population of N peaple is called to vote. There are 3 party: A, B, C.
n people are polling and the answer to a simple question:
"What party did you vote?"
In the third scenario teh election stystem is a two stage one:
Two parties with most vote pass at the second stage. 

I:"
if A loses first stage, the people vote A will vote for B with probability p1 at second stage
if B loses first stage, the people vote A will vote for C with probability p2 at second stage
if C loses first stage, the people vote A will vote for A with probability p3 at second stage"

The party with more votes ath the end of the second stage will win the election

By frequentist aproach, the probability 
P("a party will wins"|I) is computed
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import itertools
import random
import seaborn as sns

def posterior(Na, Nb):
    """
    Posterior distribuction P(Na,Nb,Nc|na,nb,nc,I)
    in the case when all the polled person says the true about the vote.

    Parameters
    ----------
    Na: integer
        number of people that vote A

    Nb: integer
        number of people that vote B

    Return
    ------
    fun: float
        Posterior distribuction P(Na,Nb,Nc|na,nb,nc,I) ù
        computed on Na, Nb
    """
    Nc = N-Na-Nb
    nc = n-na-nb
    fun = 3**(n-N)*(math.factorial(N-n))/(math.factorial(Na-na)*math.factorial(Nb-nb)*math.factorial(Nc-nc))
    return fun

def first_stage_dist(N, n, na, nb):
    """
    Retirn the posterior distribution after the first stage
    given the polled data and the background information 
    
    Parameters
    ----------
    N: integer
        number of people that vote 

    n: integer
        number of polled people

    na: integer
        number of polled people say vote A

    na: integer
        number of polled people say vote B

    Return
    ------
    fist_stage_com: list
        List of lists of all possibile combination (Na,Nb)
        given the polled data
    """
    a = np.linspace(0,N,N+1).astype(int)
    grid=[perm for perm in itertools.product(a,a)]
    print(f'len: {len(grid)}')

    tot = 0
    comb = 0
  
    im = np.zeros((N,N))
    for Na, Nb in grid:
        if (Na>=na) and (Nb>=nb) and (N-Na-Nb>=n-na-nb):
            print(f'{(Na,Nb)}: p={posterior(Na,Nb)}')
            im[Nb][Na]=posterior(Na,Nb)

            tot=tot+posterior(Na,Nb)
            comb=comb+1
            
    print(f'check total p: {"%.4f" % tot}\n')
    print(f'combination: {comb}')

    x_na,x_nb = np.where(im>0)
    fist_stage_com=[[a,b] for a,b in zip(x_na,x_nb)]
  

    return fist_stage_com

def second_stage_single_comb(N, Na, Nb, p1, p2, p3):
    """
    Given the first stage result and the polled data
    return the value of vites on the second stage 
    following the background information

    Parameters
    ----------
    N: integer
        number of people that vote 

    Na: integer
        number of people vote A on fist stage

    Nb: integer
        number of polled vote B on fist stage

    p1: float in range (0,1)

    p2: float in range (0,1)

    p3: float in range (0,1)

    Return
    ------
    NNa: integer
        a possible number of people vote for A on second stage

    NNb: integer
        a possible number of people vote for B on second stage
    """
    Nc = N-Na-Nb

    NNa = Na
    NNb = Nb
    NNc = Nc

    #A loses on first stage
    if Na<Nb and Na<N-Na-Nb:
        NNa=0
        rand=random.uniform(0,1)
        if rand<=p1:
            NNb=Nb+Na
        if rand>p1:
            NNc=Nc+Na

    #B loses on first stage
    if Nb<Na and Nb<N-Na-Nb:
        NNb=0
        rand=random.uniform(0,1)
        if rand<=p2:
            NNc=Nc+Nb
        if rand>p2:
            NNa=Na+Nc

    #c loses on first stage
    if N-Na-Nb<Na and N-Na-Nb<Nb:
        NNc=0
        rand=random.uniform(0,1)
        if rand<=p3:
            NNa=Na+Nc
        if rand>p2:
            NNb=Nb+Nc

    print(f'1 stage: A={Na}, B={Nb}, C={N-Na-Nb} - 2 stage: A={NNa}, B={NNb}, C={N-NNa-NNb}')

    return NNa,NNb

def second_stage_dist(N, n, na, nb, p1, p2, p3):
    """
    Return the distribuction of N'a, N'b, N'c 
    given a probability tthe results on fist stage, the polled data
    and the backgroung information.

    Parameters
    ----------
    N: integer
        number of people that vote 

    n: integer
        number of polled people

    na: integer
        number of polled people say vote A

    na: integer
        number of polled people say vote B
    
    p1: float in range (0,1)

    p2: float in range (0,1)

    p3: float in range (0,1)


    Returns
    -------
    im: numpy array
        Second stage distribuction P(N'a,N'b,N'c|Na,Nb,Nc,na,nb,nc,I)
    """

    a = np.linspace(0,N,N+1).astype(int)
    grid=[perm for perm in itertools.product(a,a)]
    # print(f'len: {len(grid)}')

    im = np.zeros((N,N))
    im2 = np.zeros((N,N))
    for Na, Nb in grid:
        Nc = N-Na-Nb
        nc = n-na-nb
        if (Na>=na) and (Nb>=nb) and (N-Na-Nb>=n-na-nb):
            print(f'{(Na,Nb)}: p={posterior(Na,Nb)}')
            im[Nb][Na]=posterior(Na,Nb)

            if Na<Nb and Na<Nc:
                im2[Nb+Na][0] = posterior(Na,Nb)*p1
                im2[Nb][0] = posterior(Na,Nb)*(1-p1)
                
            if Nb<Na and Nb<Nc:
                im2[0][Na] = posterior(Na,Nb)*p2
                im2[0][Na+Nc] = posterior(Na,Nb)*(1-p2)

            if Nc<Na and Nc<Nb:
                im2[Nb][Na+Nc] = posterior(Na,Nb)*p3
                im2[Nb+Nc][Na] = posterior(Na,Nb)*(1-p3)


    # comb = first_stage_dist(N, n, na, nb)

    # for a,b in comb:
    #     NNa,NNb = second_stage_single_comb(N, a, b, p1, p2, p3)
    #     print(f'1 stage: A={a}, B={b}, C={N-a-b} - 2 stage: A={NNa}, B={NNb}, C={N-NNa-NNb}')
    return im, im2
                

if __name__=="__main__":
    #Parameters
    N = 10
    n = 5
    na = 2
    nb = 1
    p1 = 0.50
    p2 = 0.50
    p3 = 0.50

    # comb= first_stage_dist(N, n, na, nb)
    second_stage_single_comb(100, 5, 20, p1, p2, p3)

    im1, im2 = second_stage_dist(N, n, na, nb, p1, p2, p3)
    print(im2.sum())

    plt.figure()
    plt.title(fr'SECOND STAGE  - $n$:{n}, $n_a$:{na}, $n_b$:{nb}, $n_c$:{n-na-nb}')
    plt.xlabel(r'$N_a$')
    plt.ylabel(r'$N_b$')
    plt.imshow(im2,cmap='bwr')
    CB  = plt.colorbar()
    plt.show()
    
   
