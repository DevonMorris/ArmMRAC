import numpy as np
import armParamHW11 as P
import control as ctrl

class armMRAC:
    # MRAC controller, estimating thetad using dirty derivative
    def __init__(self):
        self.theta_dot = 0.0          # derivative of theta
        self.theta_d1 = 0.0          # Angle theta delayed by 1 sample
        self.limit = P.tau_max         # Maxiumum force
        self.beta = P.beta           # dirty derivative gain
        self.Ts = P.Ts               # sample rate of controller

        # Reference model
        self.xref = np.matrix([0., 0.]).T # reference state
        self.Aref = P.A - P.B*P.K
        self.Bref = -self.Aref[:,0]

        # initial MRAC Gains
        self.Kx = -P.K.T                 # initial state gain
        self.Kr = -self.Aref[1,0]*P.m*P.ell**2/3                   # initial reference gain
        self.Th = -P.m*P.g*P.ell/2.

        # MRAC params
        self.Q = 1.*np.matrix([[1., 0.], [0., 1.]])
        self.P = np.matrix(ctrl.lyap(self.Aref,self.Q).T)
        self.Gammax = np.matrix([[0.001, 0.],[0., 0.001]])
        self.Gammar = 0.05
        self.GammaTh = 0.001

    def u(self, y_r, y):
        # y_r is the referenced input
        # y is the current state
        theta_r = y_r[0]
        theta = y[0]

        # differentiate theta
        self.differentiateTheta(theta)

        # Construct the state
        x = np.matrix([[theta], [self.theta_dot]])

        e = x - self.xref

        # Compute the state feedback controller
        tau_tilde = self.Kx.T*x + self.Kr*theta_r - self.Th*self.phi(x)

        # compute total torque
        tau = self.saturate(tau_tilde)

        self.adaptGains(e, x, y_r)

        return [tau.item(0)]

    def differentiateTheta(self, theta):
        '''
            differentiate theta
        '''
        self.theta_dot = self.beta*self.theta_dot + (1-self.beta)*((theta - self.theta_d1) / self.Ts)
        self.theta_d1 = theta

    def saturate(self,u):
        if abs(u) > self.limit:
            u = self.limit*np.sign(u)
        return u

    # This is not Pep8, shame on us
    def propRef(self, y_r):
        # 10 step euler integration
        N = 10
        r = y_r[0]
        for i in range(N):
            self.xref += (self.Aref*self.xref + self.Bref*r)*P.Ts/N

    def phi(self, x):
        return np.cos(x[0])

    def adaptGains(self, e, x, y_r):
        # 10 step euler integration
        r = y_r[0]
        N = 10
        for i in range(N):
            self.Kx += (self.Gammax*x*e.T*self.P*P.B)*P.Ts/N
            e[1] = 0
            self.Kr += (self.Gammar*r*e.T*self.P*P.B)*P.Ts/N
            self.Th += (self.GammaTh*self.phi(x)*e.T*self.P*P.B)*P.Ts/N

        # kind of anti-windup
        self.Kx = self.saturate(self.Kx)
        print(self.Kr)

