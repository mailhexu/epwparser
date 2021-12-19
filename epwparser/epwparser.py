import os
import sys
import re
import numpy as np
from dataclasses import dataclass


def line_to_array(line, fmt=float):
    return np.array([fmt(x) for x in line.split()])


@dataclass()
class Crystal():
    natom: int = 0
    nmode: int = 0
    nelect: float = 0.0
    at: np.ndarray = np.zeros(0)
    bg: np.ndarray = np.zeros(0)
    omega: float = 0.0
    alat: float = 0.0
    tau: np.ndarray = np.zeros(0)
    amass: np.ndarray = np.zeros(0)
    ityp: np.ndarray = np.zeros(0)
    noncolin: bool = False
    w_centers: np.ndarray = np.zeros(0)


def isTrue(s):
    return s.strip().lower().startswith("t")


def read_crystal_fmt(fname="crystal.fmt"):
    """
    parser to the crystal.fmt file
    see line 114 (qe version 6.8) epw_write in ephwann_shuffle.f90.
    """
    d = Crystal()
    with open(fname) as myfile:
        d.natom = int(next(myfile))
        d.nmode = int(next(myfile))
        d.nelect = float(next(myfile))
        d.at = line_to_array(next(myfile), float)
        d.bg = line_to_array(next(myfile), float)
        d.omega = float(next(myfile))
        d.alat = float(next(myfile))
        d.tau = line_to_array(next(myfile), float)
        d.amass = line_to_array(next(myfile), float)
        d.ityp = line_to_array(next(myfile), int)
        d.noncolin = isTrue(next(myfile))
        d.w_centers = line_to_array(next(myfile), float)
    return d


@dataclass()
class Epmat():
    Re: np.ndarray: None
    Rp: np.ndarray: None


def read_epwdata_fmt(fname="epwdata.fmt"):
    with open(fname) as myfile:
        efermi = float(next(myfile))
        nbndsub, nrr_k, nmodes, nrr_q, nrr_g = [
            int(x) for x in next(myfile).split()]
    return nbndsub, nrr_k, nmodes, nrr_q, nrr_g


def read_epmatwp(fname="./sic.epmatwp", path='./'):
    mat = np.fromfile(os.path.join(path, fname), dtype=complex)
    nbndsub, nrr_k, nmodes, nrr_q, nrr_g = read_epwdata_fmt(
        os.path.join(path, "epwdata.fmt"))
    return np.reshape(mat, (nbndsub, nbndsub, nrr_k, nmodes, nrr_g), order='F')


mat = read_epmatwp()
print(mat.shape, mat.dtype)
# epwmatwp dimensions:
# nbndsub, nbndsub, nrr_k, nmodes, nrr_g

#  ephwann_shuffle.f90  line 418
#        ALLOCATE(epmatwe(nbndsub, nbndsub, nrr_k, nmodes, nqc), STAT = ierr)
#        IF (ierr /= 0) CALL errore('ephwann_shuffle', 'Error allocating epmatwe', 1)
#        ALLOCATE(epmatwp(nbndsub, nbndsub, nrr_k, nmodes, nrr_g), STAT = ierr)
#        IF (ierr /= 0) CALL errore('ephwann_shuffle', 'Error allocating epmatwp', 1)
#        epmatwe(:, :, :, :, :) = czero
#        epmatwp(:, :, : ,: ,:) = czero


#
#     complex(dp), allocatable :: gwann(:, :, :, :, :)
#     !! e-ph vertex in Wannier representation.
#
#    if(.not. num%read_gk2 .or. .not. num%read_gq2 .or. &
#         num%plot_along_path) then
#       !Read real space matrix elements
#       call print_message("Reading Wannier rep. e-ph vertex...")
#       open(1, file = filename_epwgwann, status = 'old', access = 'stream')
#       allocate(wann%gwann(wann%numwannbands,wann%numwannbands,wann%nwsk,&
#            wann%numbranches,wann%nwsg))
#       wann%gwann = 0.0_dp
#       read(1) wann%gwann
#    end if
#    close(1)


d = read_crystal_fmt()
print(d)
