# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 23:47:57 2021

Student Name: Ceren Dumansız
Student ID  : 010160617
"""
import matplotlib.pyplot as plt
from math import cos, sin, sqrt
import pandas as pd
import numpy as np

L = []
A = []
X = []
valid = []
# Reading File
cp = pd.read_csv('controlpoints.txt', sep='\s+', names=["ID", "latitude", "longitude", "H", "h"])
tp = pd.read_csv('testpoints.txt', sep='\s+', names=["ID", "latitude", "longitude", "H", "h"])


def adjustment(cp):
    global A, X, V, L, valid
    cp = np.array(cp)

    # Creating coefficient matrix A
    for i in range(len(cp)):
        A.append([1, cos(np.radians(cp[i][1]))*cos(np.radians(cp[i][2])), cos(np.radians(cp[i][1]))*sin(np.radians(cp[i][2])), sin(np.radians(cp[i][1]))])
    A = np.matrix(A)
    AT = np.transpose(A)

    # Creating matrix L
    for i in range(len(cp)):
        L.append([cp[i][3]-cp[i][4]])

    L = np.matrix(L)

    # Creating unknowns matrix X
    X = (AT * A) ** (-1) * (AT * L)

    # Textfile including unknown matrix X
    txtfile = np.savetxt('10160617_katsayilarmatrisi.txt', A, fmt='%.5f')
    # Correction values stored in matrice V
    V = A * X - L

    # Validation
    for i in range(len(cp)):
         valid.append([sqrt((V[i] * V[i])/173)])
    valid = np.matrix(valid)
    print('m0 = %.4f m' % sum(valid))
    return A, X, V, L


adjustment(cp)


def distribution():
    datadic = []
    for i in range(len(cp)):
        fark = cp["h"][i] - cp["H"][i]
        datadic.append(float(fark))
    cp["N"] = datadic
    testdic = []
    for i in range(len(tp)):
        fark = tp["h"][i] - tp["H"][i]
        testdic.append(float(fark))
    tp["N"] = testdic
    # Plotting the distribution of control and test points
    plt.scatter(cp.latitude, cp.longitude, c=cp.N, vmin=35.975, vmax=36.825, marker='^', cmap='rainbow')
    plt.scatter(tp.latitude, tp.longitude, c=tp.N, vmin=35.975, vmax=36.825, marker='o', cmap='rainbow')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Figure 1. Distribution of control(circle) and test(triangle) points.', fontsize=8)
    cbar = plt.colorbar()
    cbar.set_label('Geoid Height in meter.')
    plt.show()
    return


distribution()


def geoid_h_diff(cp, V):
    # Plotting the height differences of test points
    V = V*100
    cp["V"] = V
    plt.scatter(cp.latitude, cp.longitude, c=cp.V, vmin=-32.5, vmax=22.5, marker='^', cmap='rainbow') 
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Figure 2. Height differences of test points.', fontsize=8)
    cbar = plt.colorbar()
    cbar.set_label('Height Differences in centimeter.')
    plt.show()
    return


geoid_h_diff(cp, V)

   