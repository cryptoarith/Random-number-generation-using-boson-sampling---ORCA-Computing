import numpy as np
import strawberryfields as sf
from strawberryfields.ops import *
import random as rn

def bsp(n=6):
    #We create an 6-mode quantum program
    boson_sampling = sf.Program(n)

    bsgPhi = [0.7804, 0.06406, 0.473, 0.563, 0.1323, 0.311, 0.4348, 0.4368]
    bsgTetha = [0.8578,  0.5165, 0.1176, 0.1517, 0.9946, 0.3231, 0.0798, 0.6157]
    rgTetha = [0.5719, -1.9782, 2.0603, 0.0644]

    phi = []
    tetha = []
    tethaR = []
    for r in range(12):
        phi.append(rn.choice(bsgPhi))
        tetha.append(rn.choice(bsgTetha))
        tethaR.append(rn.choice(rgTetha))
        
    cutoff_dim = 3
    paths = 2
    modes = 3 * paths
    initial_state = np.zeros([cutoff_dim] * modes, dtype=np.complex)
    initial_state[1, 1, 0, 1 , 1 , 0] = 1
    
    with boson_sampling.context as q:
        # prepare the input fock states
        Ket(initial_state) | q
        # rotation gates
        Rgate(tethaR[0]) | q[0]
        Rgate(tethaR[1]) | q[1]
        Rgate(tethaR[2]) | q[2]
        Rgate(tethaR[3]) | q[3]
        Rgate(tethaR[4]) | q[4]
        Rgate(tethaR[5]) | q[5]

        # beamsplitter array
        BSgate(phi[0], tetha[0]) | (q[0], q[1])
        BSgate(phi[1], tetha[0]) | (q[2], q[3])
        BSgate(phi[2], tetha[0]) | (q[4], q[5])
        BSgate(phi[3], tetha[0]) | (q[3], q[4])
        BSgate(phi[4], tetha[0]) | (q[2], q[3])
        BSgate(phi[5], tetha[0]) | (q[1], q[2])
        BSgate(phi[6], tetha[0]) | (q[0], q[1])
        BSgate(phi[7], tetha[0]) | (q[4], q[5])
        BSgate(phi[8], tetha[0]) | (q[3], q[4])
        BSgate(phi[9], tetha[0]) | (q[2], q[3])
        BSgate(phi[10], tetha[0]) | (q[1], q[2])
        BSgate(phi[11], tetha[0]) | (q[0], q[1])

    eng = sf.Engine(backend="fock", backend_options={"cutoff_dim": 3})
    #eng = sf.RemoteEngine("X8_01", backend_options={"cutoff_dim": 3})

    # We can now execute the program with the engine:
    results = eng.run(boson_sampling, shots=10000)

    # extract the joint Fock probabilities
    probs = results.state.all_fock_probs()
    #return probs
    
    modes_Probs = []
    modes_Name  = []
    modes = []

    #find the all probs that not 0 & greater than 0.01
    for i in range(0, 3):
        for j in range(0, 3):
            for k in range(0, 3):
                for l in range(0, 3):
                    for m in range(0, 3):
                        for n in range(0, 3):
                            if (probs[i, j, k, l, m, n] != 0) & (probs[i, j, k, l, m, n] > 0.01):
                                modes_Probs.append(probs[i, j, k, l, m, n])
                                modes_Name.append(
                                    "|" + str(i) + str(j) + str(k) + str(l) + str(m) + str(n) + ">")
                                #print(modes_Name[-1] + ":", probs[i, j, k, l, m, n])
                                modes.append(
                                    str(i) + str(j) + str(k) + str(l) + str(m) + str(n))
    return (modes, modes_Name, modes_Probs)
