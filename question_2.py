"""
A population of N peaple is called to vote. There are 3 party: A, B, C.
n people are polling and the answer to a simple question:
"What party did you vote?"
In the second  scenario I am not sure the interwied people say the truth.

I: "each interwied person say the truth with probability p" 

By Bayesian theory of probability and plausible reasoning, the posterior
P(Na,Nb,Nc|na,nb,nc,I) is computed
"""
import numpy as np
import matplotlib.pyplot as plt
import math
import itertools
import random
import time

def polling_sampling(n, na, nb, p):
    """
    Return one possible combination of na,nb nc
    given the polled answer. Because of the uncertainty p
    the result change every run.

    Parameters
    ----------
    n: integer
        number of interwied people

    na: integer
        number of interwied people say vote A 

    na: integer
        number of interwied people say vote B

    p: float in range(0,1)
        Probability that a person lies

    Return
    ------
    Na: integer
        a possible number of interwied people vote for A

    Nb: integer
        a possible number of interwied people vote for B

    """
    nc = n-na-nb

    Na = 0
    Nb = 0
    Nc = 0
    for i in range(na+nb+nc-1):
        if i<na:
            rand=random.uniform(0,1)
            if rand<=p:
                Na+=1
                # print(f'{i}) sono in AA - Na={Na}, Nb={Nb}, Nc={Nc}')
            else:
                rand1=random.uniform(0,1)
                if rand1<=0.5: 
                   Nb+=1
                #    print(f'{i}) sono in AB - Na={Na}, Nb={Nb}, Nc={Nc}')
                if rand1>0.5: 
                   Nc+=1
                #    print(f'{i}) sono in AC - Na={Na}, Nb={Nb}, Nc={Nc}')

        if i>=na and i<na+nb:
            rand=random.uniform(0,1)
            if rand<=p:
                Nb+=1
                # print(f'{i}) sono in BB - Na={Na}, Nb={Nb}, Nc={Nc}')
            else:
                rand1=random.uniform(0,1)
                if rand1<=0.5: 
                   Na+=1
                #    print(f'{i}) sono in BA - Na={Na}, Nb={Nb}, Nc={Nc}')
                if rand1>0.5: 
                   Nc+=1
                #    print(f'{i}) sono in BC - Na={Na}, Nb={Nb}, Nc={Nc}')
            
        if i>=na+nb-1:  
            rand=random.uniform(0,1)
            if rand<=p:
                Nc+=1
                # print(f'{i}) sono in CC - Na={Na}, Nb={Nb}, Nc={Nc}')
            else:
                rand1=random.uniform(0,1)
                if rand1<=0.5: 
                   Na+=1
                #    print(f'{i}) sono in CA - Na={Na}, Nb={Nb}, Nc={Nc}')
                if rand1>0.5: 
                   Nb+=1
                #    print(f'{i}) sono in CB - Na={Na}, Nb={Nb}, Nc={Nc}')

    return Na, Nb

def polling_distribuction(times):
    """
    Return the distribuction of na, nb, nc 
    given a probability to say the true p.

    Parameters
    ----------
    times: integer
        number of iteration used to sampling

    Return
    ------
    im: numpy array
        na, nb, nc distribuction
    """
    
    im=np.zeros((n+1,n+1))
    for time in range(times):
        a,b=polling_sampling(n,na,nb,p)
        # print(a,b)
        im[b][a]+=1
    im = im/times

    x_nb,x_na = np.where(im>0)
    print(f'total comb >0 from im :{x_na.size}')
    print(f'check for im: {np.sum(im)}')
    return im

def posterior(Na, Nb, N, n, na, nb):
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

def result_single_polling(N, n, na, nb):
    """
    Compute the focasted results for an election
    based on the polling data and the background information.
    It is the same of the first scenario.
    

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
    result: list
        list of probabilities a party will win and the tie cases
    """
    gr = np.linspace(0,N,N+1).astype(int)
    grid=[perm for perm in itertools.product(gr,gr)]
    # print(f'len: {len(grid)}')

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
            # print(f'{(Na,Nb)}: p={posterior(Na,Nb, N, n, na, nb)}')
            tot=tot+posterior(Na,Nb, N, n, na, nb)
            comb=comb+1
            
            #A wins
            if Na>Nb and Na>N-Na-Nb:
                A_win=A_win+posterior(Na,Nb, N, n, na, nb)
            #B wins
            if Nb>Na and Nb>N-Na-Nb:
                B_win=B_win+posterior(Na,Nb, N, n, na, nb)
            #C wins
            if N-Na-Nb>Na and N-Na-Nb>Nb:
                C_win=C_win+posterior(Na,Nb, N, n, na, nb)
            #ABC tie
            if Nb==Na and N-Na-Nb==Na:
                ABC_tie=ABC_tie+posterior(Na,Nb, N, n, na, nb)
            #AB tie
            if Na==Nb and Na>N-Na-Nb:
                AB_tie=AB_tie+posterior(Na,Nb, N, n, na, nb)
            #AC tie
            if Na==N-Na-Nb and Na>Nb:
                AC_tie=AC_tie+posterior(Na,Nb, N, n, na, nb)
            #BC tie 
            if Nb==N-Na-Nb and Nb>Na:
                BC_tie=BC_tie+posterior(Na,Nb, N, n, na, nb)

    print(f'combination: {comb}')
    result = [A_win,B_win,C_win,ABC_tie,AB_tie,AC_tie,BC_tie]

    return result

def result_polling(dist):
    """
    Return the forcasted result of a polling 
    in the second scenario.

    Parameters
    ----------
    dist:  numpy array
        na, nb, nc distribuction (the result of polling_distriduction)
    """
    x_nb,x_na = np.where(dist>0)
    res_list = []
   
    result_list = []
    for a,b in zip(x_na,x_nb):
        print(f'posterior: na,nb={a,b}, prob={dist[b][a]}')
        res=np.array(result_single_polling(N,n,a,b))*dist[b][a]
        result_list.append(res)
    result_list=np.vstack(result_list)

    final_res=np.sum(result_list,axis=0)
    print(f'FINAL CHECK: {np.sum(final_res)}')
    with open(f"2 scenario - N:{N}, n:{n}, na:{na}, nb:{nb}, nc:{n-na-nb}, p:{p}.txt", 'w', encoding='utf-8') as file:
        file.write(f"Data\n"
                    f"N:{N}\nn:{n}\nna:{na},\nnb:{nb}\nnc:{n-na-nb}\n"
                    f"===== RESULTS FIRST STEP =========\n"
                    f'A wins: {"%.4f" % final_res[0]}\n' 
                    f'B wins: {"%.4f" % final_res[1]}\n'
                    f'C wins: {"%.4f" % final_res[2]}\n'
                    f'ABC tie: {"%.4f" % final_res[3]}\n'
                    f'AB tie: {"%.4f" % final_res[4]}\n'
                    f'AC tie: {"%.4f" % final_res[5]}\n'
                    f'BC tie: {"%.4f" % final_res[6]}\n')
    return final_res

if __name__ == "__main__":

    #Parameters
    N = 100
    n = 20
    na = 9
    nb = 5
    p = 0.2
    
    # print(polling_sampling(n,na,nb,p))
    print("START!!!")
    start_time = time.time()

    
    im = polling_distribuction(1000000)
    x_nb,x_na = np.where(im>0)
    posterior = result_polling(im)

    end_time = time.time()

    print(posterior, end_time-start_time)

    plt.figure()
    plt.title(fr'Polling distribuction  - $n$:{n}, $n_a$:{na}, $n_b$:{nb}, $n_c$:{n-na-nb}, p={p}')
    plt.xlabel(r'$n_a$')
    plt.ylabel(r'$n_b$')
    plt.imshow(im,cmap='bwr')
    CB  = plt.colorbar()
    CB.set_label(r'$p(\tilde{n}_a,\tilde{n}_b,\tilde{n}_c|n_a,n_b,n_c,I)$')
    plt.show()



    
