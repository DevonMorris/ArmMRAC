# MRAC
Model Reference Adaptive Control (MRAC) is an adaptive control scheme that tries to mimic a reference model. MRAC does this by comparing the real system's state against some reference model and updating its control gains accordingly. This repository constitutes my efforts of understanding and implementing MRAC on a simple system. (See Robust and Adaptive Control by Lavretsky and Wise Section 9.5).

## Single-Link Robotic Arm
A single-link robotic manipulator has dynamics given by

![alt text](https://latex.codecogs.com/gif.latex?%5Cfrac%7Bd%7D%7Bdt%7D%20%5Cbegin%7Bbmatrix%7D%20%5Ctheta%20%5C%5C%20%5Cdot%7B%5Ctheta%7D%20%5Cend%7Bbmatrix%7D%20%3D%20%5Cbegin%7Bbmatrix%7D%200%20%26%201%20%5C%5C%200%20%26%20-%5Cfrac%7B3b%7D%7Bml%5E2%7D%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20%5Ctheta%20%5C%5C%20%5Cdot%7B%5Ctheta%7D%20%5Cend%7Bbmatrix%7D%20&plus;%20%5Cbegin%7Bbmatrix%7D%200%20%5C%5C%20%5Cfrac%7B3%7D%7Bml%5E2%7D%20%5Cend%7Bbmatrix%7D%20%5Cleft%28%5Ctau%20-%20mgl%5Cfrac%7B%5Ccos%7B%5Ctheta%7D%7D%7B2%7D%5Cright%29 "Single-Link Arm Dynamics")

We can see this has the general form of

![alt text](https://latex.codecogs.com/gif.latex?%5Cdot%7Bx%7D%20%3D%20Ax%20&plus;%20B%5CLambda%28u%20&plus;%20f%28x%29%29 "MRAC general form")

Furthermore, we let 

![alt text](https://latex.codecogs.com/gif.latex?f%28x%29%20%3D%20%5Cbm%7B%5CTheta%7D%5ET%5Cbm%7B%5CPhi%7D%28x%29 "Nonlinear regressor")

and 

![alt text](https://latex.codecogs.com/gif.latex?%5Cbm%7B%5CPhi%7D%28x%29%20%3D%20%5Ccos%28%5Ctheta%29 "")

## Reference Model

Since MRAC needs a reference model, we must create one. I created this by placing the poles for the linearized system about the origin. This gave me a model of the form.

![alt text](https://latex.codecogs.com/gif.latex?%5Cdot%7Bx%7D_%7Bref%7D%20%3D%20A_%7Bref%7Dx_%7Bref%7D%20&plus;%20B_%7Bref%7Dr%28t%29 "Reference Model")

## Control Law

The control law is then given by 

![alt text](https://latex.codecogs.com/gif.latex?%5Ctau%20%3D%20K_x%5ETx%20&plus;%20K_r%5ETr%20-%20%5Cbm%7B%5CTheta%7D%5ET%5Cbm%7B%5CPhi%7D%28x%29 "Control Law")

## Adaptation
To adapt the gains in the control law, we take the error between the reference and the real system given by

![alt text](https://latex.codecogs.com/gif.latex?e%20%3D%20x%20-%20x_%7Bref%7D "Error")

We also solve the Lyapunov equation given by

![alt text](https://latex.codecogs.com/gif.latex?PA_%7Bref%7D%20&plus;%20A_%7Bref%7D%5ETP%20%3D%20-Q "Algebraic Lyapunov Equation")

And adapt our gains using the MRAC laws
![alt text](https://latex.codecogs.com/gif.latex?%5Cbegin%7Baligned%7D%20K_x%20%26%3D%20-%5CGamma_x%20xe%5ET%20PB%20%5C%5C%20K_r%20%26%3D%20-%5CGamma_r%20r%28t%29e%5ET%20PB%20%5C%5C%20%5Cbm%7B%5CTheta%7D%20%26%3D%20-%5CGamma_%7B%5Ctheta%7D%20%5Cbm%7B%5CPhi%7D%28x%29e%5ET%20PB%20%5Cend%7Baligned%7D "MRAC Laws")
Where ![alt text](https://latex.codecogs.com/gif.latex?%5CGamma_x%2C%5C%20%5CGamma_r%2C%5C%20%5CGamma_%7B%5Ctheta%7D "Adaptive Gains") are the adaptive gains of the system.
