import sys
sys.path.append('..')  # add parent directory
import matplotlib.pyplot as plt
import numpy as np
import armParam as P
from armDynamics import armDynamics
from armMRAC import armMRAC
from signalGenerator import signalGenerator
from armAnimation import armAnimation
from plotData import plotData

# instantiate arm, controller, and reference classes
arm = armDynamics()
ctrl = armMRAC()
reference = signalGenerator(amplitude=30*np.pi/180.0, frequency=0.1)

# instantiate the simulation plots and animation
dataPlot = plotData()
refPlot = plotData()
animation = armAnimation()

# set disturbance input
disturbance = 0.00

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    ref_input = reference.square(t)
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        u = ctrl.u(ref_input, arm.outputs())  # Calculate the control value
        sys_input = [u[0]+ disturbance]
        arm.propagateDynamics(sys_input)  # Propagate the dynamics
        ctrl.propRef(ref_input)
        t = t + P.Ts  # advance time by Ts
    # update animation and data plots
    animation.drawArm(arm.states())
    refPlot.updatePlots(t, ref_input, ctrl.xref, u)
    dataPlot.updatePlots(t, ref_input, arm.states(), u)
    plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
