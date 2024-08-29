from nbodykit.lab import *
from nbodykit import setup_logging

import numpy as np

setup_logging("debug")

# initialize a linear power spectrum class
cosmo = cosmology.Planck15
Plin = cosmology.LinearPower(cosmo, redshift=0.55, transfer='CLASS')

# get some lognormal particles
source = LogNormalCatalog(Plin=Plin, nbar=3e-7, BoxSize=1380., Nmesh=8, seed=42)

# Define the line-of-sight direction
los = np.array([0, 0, 1])

# Apply RSD manually without using VectorProjection
# This is the projection of the velocity onto the line-of-sight direction
source['Position'] += source['VelocityOffset'] * (source['VelocityOffset'].dot(los) / np.linalg.norm(los)**2)[:, None]

# compute P(k,mu) and multipoles
result = FFTPower(source, mode='2d', poles=[0,2,4], los=los)

# and save
output = "./nbkit_example_power.json"
result.save(output)

