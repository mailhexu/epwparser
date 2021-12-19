from scipy.io import FortranFile
import numpy as np


mat = np.fromfile("./sic.epmatwp", dtype=complex)
print(mat.shape, mat.dtype)
