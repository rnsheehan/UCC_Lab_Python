#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Robert
#
# Created:     16/05/2014
# Copyright:   (c) Robert 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Import libraries
import numpy as np
import matplotlib.pyplot as plt

def sigma(p, S, xstar, B, x):
    # define the PML absorption profile
    # p defines the power of the hat function
    # S defines the amplitude of the absorption
    # xstar denotes the start location of the PML region
    # Lpml is the length of the PML region
    # x is the position at which the function is evaluated

    if xstar < B:
        if x < 0.0:
            return sigma(p, S, xstar, B, -x)
        else:
            if abs(x) < xstar:
                    return 0.0
            else:
                t1 = S*(p+1)
                t2 = (xstar - x) / (xstar - B)

                return (t2**p)*t1
    else:
        return 0.0

def main():
    pass

if __name__ == '__main__':
    main()

    # generate data for a plot
    p = 4
    S = 18.0
    xstar = 2.5
    a = -5.0
    b = 5.0

    npts = 101;
    dx = (b-a) / (npts-1)

    pos = np.zeros([npts])
    vals1 = np.zeros([npts])
    vals2 = np.zeros([npts])
    vals3 = np.zeros([npts])

    #np.zeros([len(step_size_data)])

    x = a
    for i in range(0,npts,1):
        pos[i] = x
        vals1[i] = sigma(1, S, xstar, b, x)
        vals2[i] = sigma(2, S, xstar, b, x)
        vals3[i] = sigma(4, S, xstar, b, x)
        x = x + dx

    # generate a plot of the absorption profile
    # Generate a plot of the minimum error for each computed eigenvalue
    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.plot(pos, vals1, 'r+-', label = 'p = 1')
    ax.plot(pos, vals2, 'gx-', label = 'p = 2')
    ax.plot(pos, vals3, 'bo-', label = 'p = 4')
    #ax.plot(kdata, corrminerr, 'bo-', label = 'corrected')
    ax.legend(loc='upper center')

    plt.xlabel('x', fontsize = 20)
    plt.ylabel('$\sigma(x)$', fontsize = 20)
    plt.title('Absorption profile S = %(sval)0.2f, $x^{*} = $%(xval)0.2f'%{"sval":S, "xval":xstar})
    plt.axis( [a-0.1, b+0.1, 0, 91] )

    plt.savefig('Absorption_Profile.png')

    plt.show()

    plt.clf()
    plt.cla()
    plt.close()
