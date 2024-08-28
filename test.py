from nbodykit.lab import *
from nbodykit import style
from scipy.interpolate import InterpolatedUnivariateSpline as spline

import matplotlib.pyplot as plt

redshift = 0.55
cosmo = cosmology.Planck15
Plin = cosmology.LinearPower(cosmo, redshift, transfer='EisensteinHu')
BoxSize = 1380.
Nmesh = 256

cat = LogNormalCatalog(Plin=Plin, nbar=3e-4, BoxSize=BoxSize, Nmesh=Nmesh, bias=2.0, seed=42)

# use a high-resolution mesh to get the truth
mesh = cat.to_mesh(window='tsc', Nmesh=512, compensated=True)

# compute the 1D power of this mesh
r = FFTPower(mesh, mode='1d')

# create a smooth interpolation
truth = r.power
truth = spline(truth['k'], truth['power'].real - truth.attrs['shotnoise'])

for interlaced in [True, False]:
    for window in ['CIC', 'TSC']:

        # convert catalog to a mesh with desired window and interlacing
        mesh = cat.to_mesh(Nmesh=256, window=window, compensated=False, interlaced=interlaced)

        # apply correction for the window to the mesh
        compensation = mesh.CompensateCIC if window == 'CIC' else mesh.CompensateTSC
        mesh = mesh.apply(compensation, kind='circular', mode='complex')

        # compute the 1D power P(k)
        r = FFTPower(mesh, mode='1d')
        Pk = r.power

        # compare P(k) to the hi-resolution mesh P(k)
        label = 'interlaced=%s, window=%s' %(interlaced, window)
        plt.plot(Pk['k'], (Pk['power'].real - Pk.attrs['shotnoise']) / truth(Pk['k']), label=label)


# plot Nyquist frequency
k_ny = numpy.pi * Nmesh / BoxSize
plt.axvline(x=k_ny, c='k', label="Nyquist frequency for Nmesh=256")

# format the axes
plt.legend(loc=0, ncol=2)
plt.xlabel(r"$k$ [$h \ \mathrm{Mpc}^{-1}$]")
plt.ylabel(r"$P(k) / P(k)^\mathrm{truth}$")
plt.ylim(0.9, 1.2)

