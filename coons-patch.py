import bpy
import numpy as np
from bpy import context, data, ops

arr = []
temp_arr = []
counter = 0

N = 500
def bezier_curve(p0, p1, p3, p2): 
    #p0 is endpoint 1
    #p1 is handle point 1
    #p2 is endpoint 2
    #p3 is handle point 2
    t = np.linspace(0, 1, N, endpoint=True, dtype=float)
    bezier_coordinates = []
    for s in t: 
        b0 = (1 - s) ** 3
        b1 = 3 * (1 - s) ** 2 * s
        b2 = 3 * (1 - s) * s ** 2
        b3 = s ** 3
        
        bezier_coordinates.append(b0 * p0 + b1 * p1 + b2 * p2 + b3 * p3)
    
    return np.array(bezier_coordinates)
        

with open('X:\\projects\\coons-patch\\coons_patch_points.txt') as f:
    for line in f:
        
        point = np.fromstring(line, dtype=float, sep = ' ')
        temp_arr.append(point)
        
        counter+=1
        
        if counter == 4:
            counter = 0
            arr.append(np.array(temp_arr))
            temp_arr = []
    arr = np.array(arr)

g1 = bezier_curve(arr[0][0], arr[0][1], arr[0][2], arr[0][3])
g2 = bezier_curve(arr[1][0], arr[1][1], arr[1][2], arr[1][3])
h1 = bezier_curve(arr[2][0], arr[2][1], arr[2][2], arr[2][3])
h2 = bezier_curve(arr[3][0], arr[3][1], arr[3][2], arr[3][3])

#coons patch
T = np.linspace(0, 1, N, endpoint=True, dtype=float)
S = np.linspace(0, 1, N, endpoint=True, dtype=float)

Lc = []
Ld = []
Bst = []

for s in range(len(S)):
  for t in range(len(T)):
    x = (1-T[t]) * g1[s] + g2[s] * T[t]
    y = (1-S[s]) * h1[t] + h2[t] * S[s]
    z = g1[0] * (1-S[s]) * (1-T[t]) + g1[-1] * S[s] * (1 - T[t]) + g2[0] * (1 - S[s]) * T[t] + g2[-1] * S[s] * T[t]
    Lc.append(x)
    Ld.append(y)
    Bst.append(z)

Lc = np.array(Lc)
Ld = np.array(Ld)
Bst = np.array(Bst)

Cst = Lc + Ld - Bst

Cstn = Cst.reshape(N,N,3)

faces = []

for i in range(N-1): 
    for j in range(N-1): 
        faces.append([i*N + j, i*N + j + 1, (i + 1)* N + j + 1, (i + 1)* N + j])

name = 'final_mesh'
mesh = bpy.data.meshes.new(name)
obj = bpy.data.objects.new(name, mesh)
col = bpy.data.collections.get('Collection')
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj 

mesh.from_pydata(Cst, [], faces)
