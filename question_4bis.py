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

def result_polling4(N, n, na, nb, p1, p2, p3):
    """
    Compute and print the focasted results for an election
    and return a list of probabilities distribuction of votes"
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

    for Na, Nb in grid:
        if (Na>=na) and (Nb>=nb) and (N-Na-Nb>=n-na-nb):
            # print(f'{(Na,Nb)}: p={posterior(Na,Nb)}')
            tot=tot+posterior(Na,Nb)
            comb=comb+1

            #A lose
            if Na<Nb and Na<N-Na-Nb:
                rand=random.uniform(0,1)
                if rand<=p1:
                    if Na+Nb>N-Na-Nb: B_win=B_win+posterior(Na,Nb)
                    if Na+Nb<N-Na-Nb: C_win=C_win+posterior(Na,Nb)
                    if Na+Nb==N-Na-Nb: BC_tie=BC_tie+posterior(Na,Nb)
                if rand>p1:
                    if Na+N-Na-Nb>Nb: C_win=C_win+posterior(Na,Nb)
                    if Na+N-Na-Nb<Nb: B_win=B_win+posterior(Na,Nb)
                    if Na+N-Na-Nb==Nb: BC_tie=BC_tie+posterior(Na,Nb)

            #B lose
            if Nb<Na and Nb<N-Na-Nb:
                rand=random.uniform(0,1)
                if rand<=p2:
                    if Nb+N-Na-Nb>Na: C_win=C_win+posterior(Na,Nb)
                    if Nb+N-Na-Nb<Na: A_win=A_win+posterior(Na,Nb)
                    if Nb+N-Na-Nb==Na: AC_tie=AC_tie+posterior(Na,Nb)
                if rand>p2:
                    if Nb+Na>N-Na-Nb: A_win=A_win+posterior(Na,Nb)
                    if Nb+Na<N-Na-Nb: C_win=C_win+posterior(Na,Nb)
                    if Nb+Na==N-Na-Nb: AC_tie=AC_tie+posterior(Na,Nb)


            #C lose
            if N-Na-Nb<Na and N-Na-Nb<Nb :
                rand=random.uniform(0,1)
                if rand<=p3:
                    if Na+N-Na-Nb>Nb: A_win=A_win+posterior(Na,Nb)
                    if Na+N-Na-Nb<Nb: B_win=B_win+posterior(Na,Nb)
                    if Na+N-Na-Nb==Nb: AB_tie=AB_tie+posterior(Na,Nb)
                if rand>p3:
                    if Nb+N-Na-Nb>Na: B_win=B_win+posterior(Na,Nb)
                    if Nb+N-Na-Nb<Na: A_win=A_win+posterior(Na,Nb)
                    if Nb+N-Na-Nb==Na: AB_tie=AB_tie+posterior(Na,Nb)

            #ABC tie
            if Nb==Na and N-Na-Nb==Na:
                ABC_tie=ABC_tie+posterior(Na,Nb)

            #AB tie and C wins
            if Na==Nb and N-Na-Nb>Na:
                C_win=C_win+posterior(Na,Nb)

            #BC tie and A wins
            if N-Na-Nb==Nb and Na>Nb:
                A_win=A_win+posterior(Na,Nb)

            #AC tie and B wins
            if N-Na-Nb==Na and Nb>Na:
                B_win=B_win+posterior(Na,Nb)


    # print(f'check total p: {"%.4f" % tot}\n')
    # print(f'combination: {comb}')

    with open(f"Second stage (BIS)-N:{N}, n:{n}, na:{na}, nb:{nb}, nc:{n-na-nb}", 'w', encoding='utf-8') as file:
        file.write(f"Data\n"
                   f"N:{N}\nn:{n}\nna:{na},\nnb:{nb}\nnc:{n-na-nb}\n"
                   f"===== RESULTS SECOND STEP =========\n"
                   f'A wins: {"%.4f" % A_win}\n' 
                   f'B wins: {"%.4f" % B_win}\n'
                   f'C wins: {"%.4f" % C_win}\n'
                   f'ABC tie: {"%.4f" % ABC_tie}\n'
                   f'AB tie: {"%.4f" % AB_tie}\n'
                   f'AC tie: {"%.4f" % AC_tie}\n'
                   f'BC tie: {"%.4f" % BC_tie}\n')

    # print('===== RESULTS STEP 2 =========')
    # print(f'A wins: {"%.4f" % A_win}')
    # print(f'B wins: {"%.4f" % B_win}')
    # print(f'C wins: {"%.4f" % C_win}')
    # print(f'ABC tie: {"%.4f" % ABC_tie}')
    # print(f'AB tie: {"%.4f" % AB_tie}')
    # print(f'AC tie: {"%.4f" % AC_tie}')
    # print(f'BC tie: {"%.4f" % BC_tie}')
    # print(f'check: {A_win+B_win+C_win+ABC_tie+AB_tie+AC_tie+BC_tie}')
    result = [A_win,B_win,C_win,ABC_tie,AB_tie,AC_tie,BC_tie]

    return result

    return result
if __name__ == "__main__":
    #Parameters
    N = 100
    n = 20
    na = 9
    nb = 5
    p1 = 0.30
    p2 = 0.30
    p3 = 0.30

    posterior2 = result_polling4(N, n, na, nb, p1, p2, p3)

    result_list = [result_polling4(N, n, na, nb, p1, p2, p3) for i in range (100000)]
    result_list = np.vstack(result_list)

    result_list1 = [result_polling4(N, n, na, nb, 0.999, 0.999, 0.999) for i in range (100000)]
    result_list1= np.vstack(result_list1)

    print(result_list[:,0].mean())
    
    plt.figure(f'question 4: p1={p1}, p2={p2}, p3={p3}, 0.7 and 0.2 (red)', figsize=[18, 4.8])

    plt.subplot(1,3,1)
    plt.title('A wins')
    plt.xlabel(f'mean: {"%.4f" % result_list[:,0].mean()}, mean1: {"%.4f" % result_list1[:,0].mean()}')
    sns.histplot(result_list[:,0],stat="probability",kde=True)
    sns.histplot(result_list1[:,0],stat="probability",kde=True,color='red')

    plt.subplot(1,3,2)
    plt.title('B wins')
    plt.xlabel(f'mean: {"%.4f" % result_list[:,1].mean()}, mean1: {"%.4f" % result_list1[:,1].mean()}')
    sns.histplot(result_list[:,1],stat="probability",kde=True)
    sns.histplot(result_list1[:,0],stat="probability",kde=True,color='red')

    plt.subplot(1,3,3)
    plt.title('C wins')
    plt.xlabel(f'mean: {"%.4f" % result_list[:,2].mean()}, mean1: {"%.4f" % result_list1[:,2].mean()}')
    sns.histplot(result_list[:,2],stat="probability",kde=True)
    sns.histplot(result_list1[:,0],stat="probability",kde=True,color='red')
    
    plt.show()