#!/usr/bin/env python
# coding: utf-8

# In[41]:


from qiskit import QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import RYGate
from qiskit import QuantumCircuit, execute
from qiskit import Aer
import random
from math import pi
import numpy as np


# In[42]:


mapping_dict={'00':'1','01':'2','10':'3','11':'4'}
global calls
calls=0


# In[43]:


def initial_circuit():
    backend = Aer.get_backend('unitary_simulator')
    
    circuit = QuantumCircuit(10,10)

    for i in range(10):
        rand_no=round(random.random()*1000)%2 #choose 0,1 randomly
        if rand_no==1:
            circuit.x(i)
    circuit.h(range(0,10))

    for i in range(9):
        circuit.cx(i,i+1)
    return(circuit)


# In[44]:


def angle_randomiser():
    theta_d=round(random.randrange(2,100))
    phi_d=round(random.randrange(2,100))
    lambda_d=round(random.randrange(2,100))
    theta,phi,lambd = [pi/theta_d,pi/phi_d,pi/lambda_d]
    return(theta,phi,lambd)


# In[45]:


def unitary_and_measure(circuit,theta,phi,lambd,iterations=1):
    backend = Aer.get_backend('unitary_simulator')
    m=circuit.copy()
    for repeats in range(iterations):
        m.u(theta,phi,lambd,range(0,10))
    job = backend.run(transpile(m, backend))
    res=job.result().get_unitary(m, decimals=3)
    return res


# In[46]:


def sorting_and_indexing(state_vec_rep):
    srt=sorted(set((state_vec_rep)))
    dict_indx={} #for indexing the probability amplitudes (between 0-7)
    index=0
    for num in srt:
        if index>=8:
            index=index%8
        dict_indx[num]=index
        index+=1
    dict_freq={} #for capturing the probability distribution of each index OR probability amplitude
    for num in state_vec_rep:
        if dict_indx[num] not in dict_freq.keys():
            dict_freq[dict_indx[num]]=1/1024
        else:
            dict_freq[dict_indx[num]]+=1/1024
    return(dict_freq)


# In[47]:


def dec_bin(n,dict_freq):
    try:
        val=dict_freq[n]
    except:
        val=0
    return val


# In[48]:


def circuit_bin4(theta0, theta1, theta2):
    """create |ψ2> state"""
    qc = QuantumCircuit(2, 2)
    # --- creating |ψ1> ----
    qc.ry(theta0, 0)
    # --- creating |ψ1> ----

    # === expanding |ψ1> into |ψ2> ===
    # apply RY(theta1) to the|0> state
    qc.x(0)
    qc.cry(theta1, 0, 1)
    qc.x(0)
    # apply RY(theta2) to the|1> state
    qc.cry(theta2, 0, 1)
    # === expanding |ψ1> into |ψ2> ===
    qc.measure([0, 1], [1, 0])
    return qc


# In[49]:


def food(dict_freq):
    backend = Aer.get_backend("qasm_simulator")
    shots = 1
    
    p000,p001,p010,p011,p100,p101,p110,p111 = [dec_bin(i,dict_freq) for i in range(8)]
    
    #initializing for foods
    f_p0=sum([p001,p011])/sum([p001,p011,p101,p111])
    f_p1=sum([p101,p111])/sum([p001,p011,p101,p111])
    f_p00=p001/sum([p001,p011,p101,p111])
    f_p01=p011/sum([p001,p011,p101,p111])
    f_p10=p101/sum([p001,p011,p101,p111])
    f_p11=p111/sum([p001,p011,p101,p111])

    # aggregate the distribution into two bins
    theta0 = 2 * np.arccos(np.sqrt(f_p0))
    try:
        theta1 = 2 * np.arccos(np.sqrt(f_p00 / f_p0))
    except:
        theta1=0
    try:
        theta2 = 2 * np.arccos(np.sqrt(f_p10 / f_p1))
    except:
        theta2=0

    # construct circuit and measure
    qc = circuit_bin4(theta0, theta1, theta2)
    counts = execute(qc, backend, shots=shots).result().get_counts()
    for state in counts.keys():
        return(state)


# In[50]:


def poison(dict_freq):
    backend = Aer.get_backend("qasm_simulator")
    shots = 1
    
    p000,p001,p010,p011,p100,p101,p110,p111 = [dec_bin(i,dict_freq) for i in range(8)]
        
    #initializing for poison
    p_p0=sum([p000,p010])/sum([p000,p010,p100,p110])
    p_p1=sum([p100,p110])/sum([p000,p010,p100,p110])
    p_p00=p000/sum([p000,p010,p100,p110])
    p_p01=p010/sum([p000,p010,p100,p110])
    p_p10=p100/sum([p000,p010,p100,p110])
    p_p11=p110/sum([p000,p010,p100,p110])
    
    # aggregate the distribution into two bins
    theta0 = 2 * np.arccos(np.sqrt(p_p0))
    try:
        theta1 = 2 * np.arccos(np.sqrt(p_p00 / p_p0))
    except:
        theta1=0
    try:
        theta2 = 2 * np.arccos(np.sqrt(p_p10 / p_p1))
    except:
        theta2=0

    # construct circuit and measure
    qc = circuit_bin4(theta0, theta1, theta2)
    counts = execute(qc, backend, shots=shots).result().get_counts()
    for state in counts.keys():
        return(state)


# In[51]:


def outgoing(dict_freq):
    li=[]
    for i in range(3):
        if i==1:
            li.append('food_'+mapping_dict[food(dict_freq)])
        else:
            li.append('poison_'+mapping_dict[poison(dict_freq)])
    return(li)


# In[52]:


def placement(snake_list,outgoing):
    li=[]
    li2=snake_list.copy()
    while len(li)<3:
        x=round(random.randrange(0,600))
        y=round(random.randrange(0,600))
        if [x,y] in li2:
            continue
        else:
            li.append([x,y])
            li2.append([x,y])
    li_out=[]
    for i in range(3):
        li_out.append({outgoing[i]:li[i]})
    return(li_out)


# In[53]:


def send_items(snake_list):
    global calls
    global circuit
    global theta
    global phi
    global lambd
    if calls==0:
        circuit =initial_circuit()
        theta,phi,lambd = angle_randomiser()
        unitary=unitary_and_measure(circuit,theta,phi,lambd).data
        state_vec_norm=[(x.real)**2+(x.imag)**2 for x in unitary[0]]
        dict_freq=sorting_and_indexing(state_vec_norm)
        
        fin_placed=placement(snake_list,outgoing(dict_freq))
        calls+=1
    else:
        unitary=unitary_and_measure(circuit,theta,phi,lambd,calls).data
        state_vec_norm=[(x.real)**2+(x.imag)**2 for x in unitary[0]]
        dict_freq=sorting_and_indexing(state_vec_norm)
        
        fin_placed=placement(snake_list,outgoing(dict_freq))
        calls+=1
        if calls>15:
            calls=0
    return(fin_placed)


# In[ ]:




