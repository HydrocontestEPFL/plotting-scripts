import matplotlib.pyplot as plt
import numpy as np
# import pandas

def time_index(time_data, t_ref):
    if t_ref is None:
        return None
    t_ref = time_data[0] + t_ref*1e9 # [ns]
    for i in range(len(time_data)):
        if time_data[i] > t_ref:
            return i;
    return None

# start/end time in seconds
t_start = None
t_end   = None # set to None for end

file = 'heliceprincipaletest2/_xsens_publisher_node_filter_xs_velocity.csv'

# [time_ns, x, y, z]
data = np.loadtxt(file, delimiter=';', skiprows=1, usecols=(0,5,6,7))

# print(data)
# df = pandas.read_csv(file, sep=';')
# data = df[['time_stamp', 'x', 'y', 'z']].copy().values

i_start = time_index(data[:,0], t_start)
i_end = time_index(data[:,0], t_end)

data = data[i_start:i_end]
t = (data[:,0] - data[0,0])/1e9

vel_abs = np.linalg.norm(data[:,1:3], axis=1)
plt.title('Velocity')
plt.xlabel('time [s]')
plt.ylabel('v [m/s]')
plt.plot(t, vel_abs)
#plt.show()
plt.savefig('plot_velocity.png', bbox_inches='tight')
plt.clf()
