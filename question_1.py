"""
A population of N peaple is called to vote. There are 3 party: A, B, C.
n people are polling and the answer to a simple question:
"What party did you vote?"
In the first scenario all polled individuals say the truth about their vote,
and this answer are collected.

By Bayesian theory of probability and plausible reasoning, the posterior
P(Na,Nb,Nc|na,nb,nc,I) is computed
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import itertools

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

def result_polling(N, n, na, nb):
    """
    Compute and print the focasted results for an election
    based on the polling data and the background information 
    (fist scenario).
    Create a file txt with all results

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
    im: numpy array
        Posterior distribuction P(Na,Nb,Nc|na,nb,nc,I)
    """
    a = np.linspace(0,N,N+1).astype(int)
    grid=[perm for perm in itertools.product(a,a)]
    print(f'len: {len(grid)}')

    tot = 0
    comb = 0
    A_win = 0
    B_win = 0
    C_win = 0
    ABC_tie = 0
    AB_tie = 0
    AC_tie = 0
    BC_tie = 0

    im = np.zeros((N,N))
    for Na, Nb in grid:
        if (Na>=na) and (Nb>=nb) and (N-Na-Nb>=n-na-nb):
            print(f'{(Na,Nb)}: p={posterior(Na,Nb)}')
            im[Nb][Na]=posterior(Na,Nb)

            tot=tot+posterior(Na,Nb)
            comb=comb+1
            
            #A wins
            if Na>Nb and Na>N-Na-Nb:
                A_win=A_win+posterior(Na,Nb)
            #B wins
            if Nb>Na and Nb>N-Na-Nb:
                B_win=B_win+posterior(Na,Nb)
            #C wins
            if N-Na-Nb>Na and N-Na-Nb>Nb:
                C_win=C_win+posterior(Na,Nb)
            #ABC tie
            if Nb==Na and N-Na-Nb==Na:
                ABC_tie=ABC_tie+posterior(Na,Nb)
            #AB tie
            if Na==Nb and Na>N-Na-Nb:
                AB_tie=AB_tie+posterior(Na,Nb)
            #AC tie
            if Na==N-Na-Nb and Na>Nb:
                AC_tie=AC_tie+posterior(Na,Nb)
            #BC tie 
            if Nb==N-Na-Nb and Nb>Na:
                BC_tie=BC_tie+posterior(Na,Nb)

    print(f'check total p: {"%.4f" % tot}\n')
    print(f'combination: {comb}')

    with open(f"First step-N:{N}, n:{n}, na:{na}, nb:{nb}, nc:{n-na-nb}.txt", 'w', encoding='utf-8') as file:
        file.write(f"Data\n"
                   f"N:{N}\nn:{n}\nna:{na},\nnb:{nb}\nnc:{n-na-nb}\n"
                   f"===== RESULTS FIRST STEP =========\n"
                   f'A wins: {"%.4f" % A_win}\n' 
                   f'B wins: {"%.4f" % B_win}\n'
                   f'C wins: {"%.4f" % C_win}\n'
                   f'ABC tie: {"%.4f" % ABC_tie}\n'
                   f'AB tie: {"%.4f" % AB_tie}\n'
                   f'AC tie: {"%.4f" % AC_tie}\n'
                   f'BC tie: {"%.4f" % BC_tie}\n')

    print('===== RESULTS =========')
    print(f'A wins: {"%.4f" % A_win}')
    print(f'B wins: {"%.4f" % B_win}')
    print(f'C wins: {"%.4f" % C_win}')
    print(f'ABC tie: {"%.4f" % ABC_tie}')
    print(f'AB tie: {"%.4f" % AB_tie}')
    print(f'AC tie: {"%.4f" % AC_tie}')
    print(f'BC tie: {"%.4f" % BC_tie}')
    print(f'check: {A_win+B_win+C_win+ABC_tie+AB_tie+AC_tie+BC_tie}')

    return im



if __name__ == "__main__":
    #Parameters
    N = 100
    n = 20
    na = 9
    nb = 5
    
    posterior = result_polling(N,n,na,nb)

    plt.figure()
    plt.title(fr'First step  -  $N$:{N},  $n$:{n}, $n_a$:{na}, $n_b$:{nb}, $n_c$:{n-na-nb}')
    plt.imshow(posterior,cmap='bwr')
    plt.xlabel(r'$N_a$')
    plt.ylabel(r'$N_b$')
    CB  = plt.colorbar()
    CB.set_label(r'$p(N_a,N_b|N,n_a,n_b,n_c,I)$')

    plt.show()
            




    
