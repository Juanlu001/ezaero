"""
Dihedral angle effect
=====================

Effect of dihedral on the lift coefficient slope of rectangular wings.

References
----------
.. [1] Katz, J. et al., *Low-Speed Aerodynamics*, 2nd ed, Cambridge University
   Press, 2001: figure 12.21
"""
import time

import matplotlib.pyplot as plt
import numpy as np

import ezaero.vlm.steady as vlm

start = time.time()

# dihedral angles grid
deltas = np.array([-45, -30, -15, 0, 15, 30]) * np.pi / 180

# define mesh parameters and flight conditions
mesh = vlm.MeshParams(m=8, n=30)
# slope for each dihedral calculated using two flight conditions
flcond_0 = vlm.FlightConditions(ui=100.0, alpha=0.0, rho=1.0)
flcond_1 = vlm.FlightConditions(ui=100.0, alpha=np.pi / 180, rho=1.0)
cla_list = []  # container for the lift coefficient slope
for delta in deltas:
    # The figure in the book uses an aspect ratio of 4. It does not
    # correspond to the planform, but the "real" wingspan, hence we project
    # the wingspan with the dihedral angle
    bp = 4 * np.cos(delta)
    # define rectangular wing (same cr and ct), with no sweep (theta).
    wing = vlm.WingParams(cr=1.0, ct=1.0, bp=bp, theta=0, delta=delta)
    res_0 = vlm.run_simulation(wing=wing, mesh=mesh, flcond=flcond_0)
    res_1 = vlm.run_simulation(wing=wing, mesh=mesh, flcond=flcond_1)
    d_cl = res_1['cl_wing'] - res_0['cl_wing']
    d_alpha = flcond_1.alpha - flcond_0.alpha
    slope = d_cl / d_alpha * np.cos(delta)  # project load
    cla_list.append(slope)

end = time.time()
elapsed = end - start

print('Elapsed time: {} s'.format(elapsed))

fig = plt.figure()
plt.plot(deltas * 180 / np.pi, cla_list, 'o-')
plt.xlabel(r'$\delta$[deg]')
plt.ylabel(r'CL$_\alpha$')
plt.ylim(0, 4)
plt.grid()
plt.xlim(deltas.min() * 180 / np.pi, deltas.max() * 180 / np.pi)
plt.show()
