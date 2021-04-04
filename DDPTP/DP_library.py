import numpy as np

def get_laplace_noise(sensitivity,epsilon):
    beta = sensitivity/epsilon
    u1 = np.random.random()
    u2 = np.random.random()
    if u1 <= 0.5:
        noise = -beta*np.log(1.-u2)
    else:
        noise = beta*np.log(u2)
    return noise
  
def laplace(data,sensitivity=1,epsilon=1):
    data = float(data)+get_laplace_noise(sensitivity,epsilon)
    return data