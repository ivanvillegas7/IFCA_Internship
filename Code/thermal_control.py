# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 20:19:16 2023

@author: Iván Villegas Pérez

The script then defines a list called experiments that contains the names of
four different experiments.

The script then computes the absorbed power for a given experiment. Depending
of which experiment is being studied, different parameters get different values
plotting the computed absorved power as a function of the temperature in the
sensor, to know if it will saturate or not. 
"""

#Import different packages

import numpy as np

from typing import List

import matplotlib.pyplot as plt

import best_fit

#Studied experiments

experiments: List[str] = ['QUIJOTE', 'CLASS', 'ACT', 'LSPE-STRIP']

def absorved_power(A_p: float, freq: float, T: np.array(float),\
                   A_r: float):
    
    """
    Calculates the absorbed power of a receiver given the following parameters:
    
    Parameters:
    - A_p (float): Effective collecting area of the receiver, in m^2
    - epsilon (float): Emissivity of the receiver
    - freq (float): Frequency of the radiation, in GHz
    - T (1D array): Temperature of the receiver as a function of time, in
                    degrees Celsius
    - A_r (float): Area of the reflector, in m^2
    
    Returns:
    - power (1D array): the absorbed power of the receiver, in pW
    
    """
    
    k_B: float = 1.380649e-23#J/K
    
    c: float = 3e8#m/s
    
    d: float = 4e5#m
    
    epsilon: float = 0.3
    
    #
    
    power: np.array(float) = (A_r/2)**2*np.pi*k_B*(3*epsilon+epsilon**3/4)*\
                             (freq*1e9)**3*(A_p/(2*d))**2*(T+273.15)*1e12/(6*c**2)
    
    return power

def thermal_control(experiment: str):
    
    """
    Plots the absorbed power by the telescope at different temperatures for a
    given experiment.

    Parameters:
    - experiment (str): The name of the experiment.
    
    Returns:
        
        None

    """
    
    #Check which experiment is going to be studied

    if experiment == experiments[0]:
        
        #Telescope aperture

        A_p: float = 2.25
        
        #Observed frequencies
        
        freq: List[float] = [11, 13, 17, 19, 30, 40]
        
        #Antenna diameter
        
        A_r: List[float] = [0.175, 0.156, 0.132, 0.132, 0.074, 0.064]

    elif experiment == experiments[1]:
        
        #Telescope aperture

        A_p: float = 0.46

        #Observed frequencies
        
        freq: List[float] = [40, 90, 150, 220]
        
        #Antenna diameter
        
        A_r: List[float] = [0.064, 0.053, 0.037, best_fit.best_fit(220)]
        
        print(f"\nLast angular aperture for {experiment} is {A_r[-1]}.\n")
        
    elif experiment == experiments[2]:
        
        #Telescope aperture

        A_p: float = 6
        
        #Observed frequencies
        
        freq: List[float] = [28, 41, 90, 150, 230]
        
        #Antenna diameter
        
        A_r: List[float] = [0.1, 0.064, 0.053, 0.037, best_fit.best_fit(230)]
        
        print(f"\nLast angular aperture for {experiment} is {A_r[-1]}.\n")
        
    elif experiment == experiments[3]:
        
        #Telescope aperture

        A_p: float = 1.5
        
        #Observed frequencies
        
        freq: List[float] = [43, 95]
        
        #Antenna diameter
        
        A_r: List[float] = [0.064, 0.053]
        
    T: np.array(float) = np.linspace(0, 200, 200)
    
    plt.figure()
    
    for i in range(len(freq)):
        
        plt.plot(T, absorved_power(A_p, freq[i], T, A_r[i]),\
                 label=f'{freq[i]} GHz')
        
    plt.yscale("log")
    plt.xlabel('Temperature [°C]')
    plt.ylabel('Absorbed power [pW]')
    plt.title(f"{experiment}'s absorbed power against temperature")
    plt.legend()
    plt.grid(True)
    plt.savefig(f'../Python Plots/{experiment}/{experiment} AbsorbedPower vs Temperature.pdf')
