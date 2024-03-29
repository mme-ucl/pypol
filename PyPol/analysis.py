# TODO Remove
# import numpy as np
# import os
# import matplotlib.pyplot as plt
# import progressbar
# import pandas as pd
# import itertools as its
# import copy
# from typing import Union
# from sklearn.neighbors import KernelDensity as KDE
#
# from PyPol.utilities import get_list_crystals
# from PyPol.crystals import Molecule
# from PyPol.gromacs import EnergyMinimization, MolecularDynamics, CellRelaxation, Metadynamics
# from PyPol.fingerprints import *
# from PyPol.walls import *
# from PyPol.groups import *
# from PyPol.metad import _MetaCV, Density, PotentialEnergy
# from PyPol.cluster import *


#
# Distributions
#
#
#
# class _CollectiveVariable(object):  # TODO Change name to Distributions
#     """
#     General Class for Collective Variables.
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - clustering_type: How is it treated by clustering algorithms.
#     - kernel: kernel function to use in the histogram generation.
#     - bandwidth: the bandwidths for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_max: the upper bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     - timeinterval: Simulation time interval to generate the distribution.
#     """
#
#     def __init__(self, name: str, cv_type: str, plumed: str, clustering_type="distribution", kernel="TRIANGULAR",
#                  bandwidth: Union[float, list, tuple] = None,
#                  grid_min: Union[float, list, tuple] = None,
#                  grid_max: Union[float, list, tuple] = None,
#                  grid_bins: Union[int, list, tuple] = None,
#                  grid_space: Union[float, list, tuple] = None,
#                  timeinterval: Union[float, tuple] = None):
#         """
#         General Class for Collective Variables.
#         :param name: name of the CV.
#         :param cv_type: Type of the CV.
#         :param plumed: Command line for plumed.
#         :param clustering_type: How is it treated by clustering algorithms.
#         :param kernel: kernel function to use in the histogram generation.
#         :param bandwidth: the bandwidths for kernel density estimation.
#         :param grid_min: the lower bounds for the grid.
#         :param grid_max: the upper bounds for the grid.
#         :param grid_bins: the number of bins for the grid.
#         :param grid_space: the approximate grid spacing for the grid.
#         :param timeinterval: Simulation time interval to generate the distribution.
#         """
#         self._name = name
#         self._type = cv_type
#         self._clustering_type = clustering_type
#
#         self._kernel = kernel
#         self._bandwidth = bandwidth
#
#         self._grid_min = grid_min
#         self._grid_max = grid_max
#         self._grid_bins = grid_bins
#         self._timeinterval = timeinterval
#         self._grid_space = grid_space
#         self._plumed = plumed
#
#     @property
#     def kernel(self):
#         return self._kernel
#
#     @kernel.setter
#     def kernel(self, kernel: str):
#         if kernel.upper() in ("GAUSSIAN", "TRIANGULAR"):
#             self._kernel = kernel
#         else:
#             print("Kernel function not recognized. Choose between 'GAUSSIAN' and 'TRIANGULAR'.")
#
#     @property
#     def timeinterval(self):
#         return self._timeinterval
#
#     @timeinterval.setter
#     def timeinterval(self, time: float, time2: float = None):
#         if time2:
#             self._timeinterval = (time, time2)
#         else:
#             self._timeinterval = time
#
#     @property
#     def bandwidth(self):
#         return self._bandwidth
#
#     @bandwidth.setter
#     def bandwidth(self, bandwidth: float):
#         if self._grid_space < bandwidth * 0.5:
#             self._bandwidth = bandwidth
#         else:
#             print("""
# The bin size must be smaller than half the bandwidth. Choose a bandwidth greater than {}.
# Alternatively, you can change the bin space or the number of bins.""".format(self._grid_space * 2))
#
#     @property
#     def grid_min(self):
#         return self._grid_min
#
#     @grid_min.setter
#     def grid_min(self, grid_min: float):
#         self._grid_min = grid_min
#         self.grid_space = self._grid_space
#
#     @property
#     def grid_max(self):
#         return self._grid_max
#
#     @grid_max.setter
#     def grid_max(self, grid_max: float):
#         self._grid_max = grid_max
#         self.grid_space = self._grid_space
#
#     @property
#     def grid_bins(self):
#         return self._grid_bins
#
#     @grid_bins.setter
#     def grid_bins(self, grid_bins: int):
#         self._grid_bins = grid_bins
#         if self._grid_max:
#             self._grid_space = (self._grid_max - self._grid_min) / float(self._grid_bins)
#             if self._grid_space > self._bandwidth * 0.5:
#                 print("The bin size must be smaller than half the bandwidth. Please change the bandwidth accordingly.")
#
#     @property
#     def grid_space(self):
#         return self._grid_space
#
#     @grid_space.setter
#     def grid_space(self, grid_space: float):
#         self._grid_space = grid_space
#         if self._grid_space > self._bandwidth * 0.5:
#             print("The bin size must be smaller than half the bandwidth. Please change the bandwidth accordingly.")
#         if self._grid_max:
#             self._grid_bins = int((self._grid_max - self._grid_min) / self._grid_space)
#
#     # Read-only properties
#     @property
#     def type(self):
#         return self._type
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def clustering_type(self):
#         return self._clustering_type
#
#     def __str__(self):
#         if self._grid_max:
#             txt = """
# CV: {0._name} ({0._type})
# Clustering Type: {0._clustering_type}
# Plumed command: {0._plumed}
# KERNEL={0._kernel} BANDWIDTH={0._bandwidth:.3f}
# NBINS={0._grid_bins} GRIDSPACE={0._grid_space:.3f} UPPER={0._grid_max:.3f} LOWER={0._grid_min:.3f}""".format(self)
#         else:
#             txt = """
# CV: {0._name} ({0._type})
# Clustering Type: {0._clustering_type}
# Plumed command: {0._plumed}
# KERNEL={0._kernel} BANDWIDTH={0._bandwidth:.3f} GRIDSPACE={0._grid_space:.3f}""".format(self)
#         return txt
#
#
# class Torsions(_CollectiveVariable):
#     """
#     Generates a distribution of the torsional angles of the selected atoms.
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - plumed: Command line for plumed.
#     - clustering_type: How is it treated by clustering algorithms.
#     - kernel: kernel function to use in the histogram generation.
#     - bandwidth: the bandwidths for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_max: the upper bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     - timeinterval: Simulation time interval to generate the distribution.
#     - atoms: the 4 atom index of the molecular forcefield object used to generate the set of torsional angles
#     - molecule: the molecular forcefield object from which atoms are selected
#
#     Methods:\n
#     - help(): Print attributes and methods
#     - set_atoms(atoms, molecule): Select the 4 atom index from the Molecule obj to generate the set of torsional angles
#     - generate_input(simulation, bash_script=True): Generate the plumed input files
#     - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#     """
#
#     def __init__(self, name: str, plumed: str):
#         """
#         Generates a distribution of the torsional angles of the selected atoms.
#         :param name: str, name of the collective variable. Default output and variables will have this name.
#         :param plumed: command line for the plumed file.
#         """
#         super().__init__(name=name,
#                          cv_type="Torsional Angle",
#                          plumed=plumed,
#                          clustering_type="distribution",
#                          kernel="TRIANGULAR",
#                          bandwidth=0.25,
#                          grid_bins=73,
#                          grid_min=-np.pi,
#                          grid_max=np.pi,
#                          grid_space=2 * np.pi / 73,
#                          timeinterval=200)
#
#         self._atoms = list()
#         self._molecule = None
#
#     @property
#     def atoms(self):
#         return self._atoms
#
#     @atoms.setter
#     def atoms(self, atoms):
#         if len(atoms) == 4:
#             self._atoms = atoms
#         else:
#             print("Error: Torsional Angles needs 4 atoms as input")
#
#     @property
#     def molecule(self):
#         return self._molecule
#
#     @molecule.setter
#     def molecule(self, molecule):
#         self._molecule = molecule
#
#     @staticmethod
#     def help():
#         return """
# Calculate the distribution of a set of torsional angles.
# It creates the inputs for plumed and stores the results.
#
# Attributes:
# - name: name of the CV.
# - type: Type of the CV (Torsional Angle).
# - plumed: Command line for plumed.
# - clustering_type: How is it treated by clustering algorithms (distribution).
# - kernel: kernel function to use in the histogram generation. It can be "TRIANGULAR" or "GAUSSIAN"
# - bandwidth: the bandwidths for kernel density estimation. The bin size must be smaller than half the bandwidth.
# - grid_min: the lower bounds for the grid.
# - grid_max: the upper bounds for the grid.
# - grid_bins: the number of bins for the grid.
# - grid_space: the approximate grid spacing for the grid.
# - timeinterval: Simulation time interval to generate the distribution.
#                 If a single value is given, t, frames corresponding to the last "t" picoseconds are used.
#                 If two values are given, t1 and t2, frames from time t1 to time t2 are used.
# - atoms: the 4 atom index of the molecular forcefield object used to generate the set of torsional angles.
#                 The same torsional angle in each molecule of the crystal will be considered for the distribution.
# - molecule: the molecular forcefield object from which atoms are selected.
#
# Methods:
# - help(): Print attributes and methods
# - set_atoms(atoms, molecule): Select the 4 atom index from the Molecule obj to generate the set of torsional angles.
#                 The atom index in PyPol starts from 0 and can be seen in the
# - generate_input(simulation, bash_script=True): Generate the plumed input files
# - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#                 If crystal="all", results are stored for all crystals. Alternatively, you can select a subset of
#                 crystals by specifying their IDs in an iterable object.
#                 If plot=True, a plot of the distribution is created. This could be slow for large sets.
#
# Examples:
# - Select atoms of the torsional angles and create plumed inputs:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# tor = gaff.get_cv("tor")                                      # Retrieve the CV Object
# tor.set_atoms((0, 1, 2, 3), molecule)                         # Use the first four atoms to define the torsional angle
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# tor.generate_input(npt)                                       # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project
#
# - Import distributions once the plumed driver analysis is finished:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# tor = gaff.get_cv("tor")                                      # Retrieve the CV Object
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# tor.get_results(npt, plot=False)                              # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project"""
#
#     def set_atoms(self, atoms: Union[list, tuple], molecule: Molecule):
#         """
#         Select atom indices of the reference molecule. This is used to identify the torsions of each molecule in the
#         crystal.
#         :param atoms: list, Atom indices. All atoms indices are available in the project output file after the topology
#         is defined.
#         :param molecule: obj, Reference molecule
#         :return:
#         """
#         self.atoms = atoms
#         self.molecule = molecule
#
#     def generate_input(self,
#                        simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#                        bash_script=True,
#                        crystals="all",
#                        catt=None,
#                        matt=None):
#         """
#         Generate the plumed input files. If the catt option is used, only crystals with the specified attribute are
#         used. If the matt option is used only molecules with the specified attributes are used. In both cases,
#         attributes must be specified in the form of a python dict, menaning catt={"AttributeLabel": "AttributeValue"}.
#
#         :param simulation: Simulation object
#         :param bash_script: If True, generate a bash script to run simulations
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :param matt: Use Molecular attributes to select the molecules list
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#
#         if not self._atoms:
#             print("Error: no atoms found. select atoms with the set_atoms module.")
#             exit()
#         print("=" * 100)
#         print(self.__str__())
#
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#
#         for crystal in list_crystals:
#             print(crystal._name)
#             lines_atoms = generate_atom_list(self._atoms, self._molecule, crystal, keyword="ATOMS", lines=[],
#                                              attributes=matt)
#             file_plumed = open(crystal._path + "plumed_" + self._name + ".dat", "w")
#             file_plumed.write("TORSIONS ...\n")
#             for line in lines_atoms:
#                 file_plumed.write(line)
#
#             file_plumed.write("HISTOGRAM={{{{{0._kernel} NBINS={0._grid_bins} BANDWIDTH={0._bandwidth:.3f} "
#                               "UPPER={0._grid_max:.3f} LOWER={0._grid_min:.3f}}}}}\n".format(self))
#
#             file_plumed.write("LABEL={0}\n... TORSIONS\n\n"
#                               "PRINT ARG={0}.* FILE=plumed_{1}_{0}.dat\n".format(self._name, simulation._name))
#             file_plumed.close()
#
#         if bash_script:
#             dt, nsteps, traj_stride, traj_start, traj_end = (None, None, None, None, None)
#
#             file_mdp = open(simulation._path_mdp)
#             for line in file_mdp:
#                 if line.startswith('dt '):
#                     dt = float(line.split()[2])
#                 elif line.startswith(("nstxout", "nstxout-compressed")):
#                     traj_stride = int(line.split()[2])
#                 elif line.startswith('nsteps '):
#                     nsteps = float(line.split()[2])
#             file_mdp.close()
#
#             traj_time = int(nsteps * dt)
#             if traj_time > 0:
#                 if isinstance(self._timeinterval, tuple):
#                     traj_start = self._timeinterval[0]
#                     traj_end = self._timeinterval[1]
#                 elif isinstance(self._timeinterval, int):
#                     traj_start = traj_time - self._timeinterval
#                     traj_end = traj_time
#                 else:
#                     print("Error: No suitable time interval.")
#                     exit()
#
#             file_script = open(simulation._path_data + "/run_plumed_" + self._name + ".sh", "w")
#             file_script.write('#!/bin/bash\n\n'
#                               'crystal_paths="\n')
#             for crystal in list_crystals:
#                 file_script.write(crystal._path + "\n")
#
#             if isinstance(simulation, Metadynamics):
#                 file_script.write('"\n\n'
#                                   'for crystal in $crystal_paths ; do\n'
#                                   'cd "$crystal" || exit \n'
#                                   '#{0} trjconv -f {1}.xtc -o plumed_{1}.xtc -s {1}.tpr -b {2} -e {3} <<< 0\n'
#                                   '{4} driver --mf_xtc plumed_{1}.xtc --plumed plumed_{5}.dat --timestep {6} '
#                                   '--trajectory-stride {7} --mc mc.dat\n'
#                                   '#rm plumed_{1}.xtc\n'
#                                   'done\n'
#                                   ''.format(simulation._gromacs, simulation._name, traj_start, traj_end,
#                                             self._plumed, self._name, dt, traj_stride))
#                 file_script.close()
#             else:
#                 file_script.write('"\n\n'
#                                   'for crystal in $crystal_paths ; do\n'
#                                   'cd "$crystal" || exit \n'
#                                   '{0} trjconv -f {1}.xtc -o plumed_{1}.xtc -s {1}.tpr -b {2} -e {3} <<< 0\n'
#                                   '{4} driver --mf_xtc plumed_{1}.xtc --plumed plumed_{5}.dat --timestep {6} '
#                                   '--trajectory-stride {7} --mc mc.dat\n'
#                                   'rm plumed_{1}.xtc\n'
#                                   'done\n'
#                                   ''.format(simulation._gromacs, simulation._name, traj_start, traj_end,
#                                             self._plumed, self._name, dt, traj_stride))
#                 file_script.close()
#         print("=" * 100)
#
#     @staticmethod
#     def get_from_file(path, name=None):
#         cv = np.genfromtxt(path, skip_header=1)[:, 1:]
#         if np.isnan(cv).any():
#             cv = np.nanmean(cv, axis=0)
#             if np.isnan(cv).any():
#                 print(f"\nError: NaN values present in final distribution of crystal {name}. Check {path}")
#                 exit()
#             print(f"\nWarning: NaN values present in some frames of crystal {name}. Check {path}")
#         else:
#             cv = np.average(cv, axis=0)
#         cv /= cv.sum()
#         return cv
#
#     def get_results(self,
#                     simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#                     crystals: Union[str, list, tuple] = "all",
#                     plot: bool = True, catt=None):
#         """
#         Verify if the distribution has been correctly generated and store the result. If the distribution is taken over
#         different frames, the average is calculated.
#         :param simulation: Simulation object
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :param plot: If true, generate a plot of the distribution.
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#         print("\n" + str(self._name))
#         bar = progressbar.ProgressBar(maxval=len(list_crystals)).start()
#         nbar = 1
#         for crystal in list_crystals:
#             path_plumed_output = crystal._path + "plumed_{}_{}.dat".format(simulation._name, self._name)
#             if os.path.exists(path_plumed_output):
#                 # cv = np.genfromtxt(path_plumed_output, skip_header=1)[:, 1:]
#                 # if np.isnan(cv).any():
#                 #     cv = np.nanmean(cv, axis=0)
#                 #     if np.isnan(cv).any():
#                 #         print("\nError: NaN values present in final distribution of crystal {0._name}. Check {0._path} "
#                 #               "".format(crystal))
#                 #         exit()
#                 #     print("\nWarning: NaN values present in some frames of crystal {0._name}. Check {0._path} "
#                 #           "".format(crystal))
#                 # else:
#                 #     cv = np.average(cv, axis=0)
#                 # cv /= cv.sum()
#                 cv = self.get_from_file(path_plumed_output, crystal._name)
#                 crystal._cvs[self._name] = cv
#                 # Save output and plot distribution
#                 x = np.linspace(self._grid_min, self._grid_max, len(cv))
#                 np.savetxt(crystal._path + "plumed_{}_{}_data.dat".format(simulation._name, self._name),
#                            np.column_stack((x, cv)), fmt=("%1.3f", "%1.5f"),
#                            header="Angle ProbabilityDensity")
#                 if plot:
#                     plt.plot(x, crystal._cvs[self._name], "-")
#                     plt.xlabel("Torsional Angle / rad")
#                     plt.xlim(self._grid_min, self._grid_max)
#                     plt.ylabel("Probability Density")
#                     plt.savefig(crystal._path + "plumed_{}_{}_plot.png".format(simulation._name, self._name), dpi=300)
#                     plt.close("all")
#                 bar.update(nbar)
#                 nbar += 1
#             else:
#                 print("An error has occurred with Plumed. Check file {} in folder {}."
#                       "".format(path_plumed_output, crystal._path))
#         bar.finish()
#
#     def __str__(self):
#         txt = super(Torsions, self).__str__()
#         if self._atoms:
#             txt += "\nAtoms:  "
#             for atom in self._atoms:
#                 txt += "{}({})  ".format(atom, self._molecule._atoms[atom]._label)
#         else:
#             txt += "No atoms found in CV {}. Select atoms with the 'set_atoms' module.\n".format(self._name)
#         txt += "\n"
#         return txt
#
#     def _write_output(self, path_output):
#         file_output = open(path_output, "a")
#         file_output.write(self.__str__())
#         file_output.close()
#
#
# class MolecularOrientation(_CollectiveVariable):
#     """
#     Generates a distribution of the intermolecular torsional angles of the selected atoms.
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - plumed: Command line for plumed.
#     - clustering_type: How is it treated by clustering algorithms.
#     - kernel: kernel function to use in the histogram generation.
#     - bandwidth: the bandwidths for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_max: the upper bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     - timeinterval: Simulation time interval to generate the distribution.
#     - atoms: the 2 atom index of the molecular forcefield object used to generate the set of orientational vectors
#     - molecules: the molecular forcefield object from which atoms are selected
#
#     Methods:\n
#     - help(): Print attributes and methods
#     - set_atoms(atoms, molecule): Select the 4 atom index from the Molecule obj to generate the set of torsional angles
#     - generate_input(simulation, bash_script=True): Generate the plumed input files
#     - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#     """
#
#     def __init__(self, name, plumed):
#         """
#         Generates a distribution of the intermolecular torsional angles of the selected atoms.
#         :param name: str, name of the collective variable. Default output and variables will have this name.
#         """
#         super().__init__(name=name,
#                          cv_type="Molecular Orientation",
#                          plumed=plumed,
#                          clustering_type="distribution",
#                          kernel="TRIANGULAR",
#                          bandwidth=0.25,
#                          grid_min=0.0,
#                          grid_max=np.pi,
#                          grid_bins=37,
#                          grid_space=np.pi / 37,
#                          timeinterval=200)
#
#         self._atoms = list()
#         self._molecules = list()
#
#     @property
#     def atoms(self):
#         return self._atoms
#
#     @property
#     def molecules(self):
#         return self._molecules
#
#     def __str__(self):
#         txt = super(MolecularOrientation, self).__str__()
#         if self._atoms:
#             for idx_mol in range(len(self._molecules)):
#                 txt += "\nMolecule '{}': ".format(self._molecules[idx_mol]._residue)
#                 for atom in self._atoms[idx_mol]:
#                     txt += "{}({})    ".format(atom, self._molecules[idx_mol]._atoms[atom]._label)
#             txt += "\n"
#         else:
#             txt += "No atoms found in CV {}. Select atoms with the 'set_atoms' module.\n".format(self._name)
#         return txt
#
#     @staticmethod
#     def help():
#         return """
# Calculate the distribution of a set of torsional angles.
# It creates the inputs for plumed and stores the results.
#
# Attributes:
# - name: name of the CV.
# - type: Type of the CV (Torsional Angle).
# - plumed: Command line for plumed.
# - clustering_type: How is it treated by clustering algorithms (distribution).
# - kernel: kernel function to use in the histogram generation. It can be "TRIANGULAR" or "GAUSSIAN"
# - bandwidth: the bandwidths for kernel density estimation. The bin size must be smaller than half the bandwidth.
# - grid_min: the lower bounds for the grid.
# - grid_max: the upper bounds for the grid.
# - grid_bins: the number of bins for the grid.
# - grid_space: the approximate grid spacing for the grid.
# - timeinterval: Simulation time interval to generate the distribution.
#                 If a single value is given, t, frames corresponding to the last "t" picoseconds are used.
#                 If two values are given, t1 and t2, frames from time t1 to time t2 are used.
# - atoms: the 2 atom index of the molecular forcefield object used to generate the set of orientational vectors
# - molecules: the molecular forcefield object from which atoms are selected
#
# Methods:
# - help(): Print attributes and methods
# - set_atoms(atoms, molecule): Select the 2 atom index from the Molecule obj to generate the orientational vectors.
#                 The atom index in PyPol starts from 0 and can be seen in the
# - generate_input(simulation, bash_script=True): Generate the plumed input files
# - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#                 If crystal="all", results are stored for all crystals. Alternatively, you can select a subset of
#                 crystals by specifying their IDs in an iterable object.
#                 If plot=True, a plot of the distribution is created. This could be slow for large sets.
#
# Examples:
# - Select atoms of the orientational vectors and create plumed inputs:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# mo = gaff.get_cv("mo")                                        # Retrieve the CV Object
# mo.set_atoms((0, 1), molecule)                                # Use the first two atoms to define the orientational vect
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# mo.generate_input(npt)                                        # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project
#
# - Import distributions once the plumed driver analysis is finished:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# mo = gaff.get_cv("mo")                                        # Retrieve the CV Object
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# mo.get_results(npt, plot=False)                               # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project
#
# - Check orientational disorder:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# mo = gaff.get_cv("mo")                                        # Retrieve the CV Object
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# mo.identify_orientational_disorder(npt)                       # Identify melted structures
# project.save()                                                # Save project"""
#
#     def set_atoms(self, atoms: Union[list, tuple], molecule: Molecule):
#         """
#         :param atoms:
#         :param molecule:
#         :return:
#         """
#         if len(atoms) == 2 and molecule not in self._molecules:
#             self._atoms.append(list(atoms))
#             self._molecules.append(molecule)
#
#     # TODO Introduce this method after multiple molecular forcefields can be used
#     # def remove_atoms(self, index="all"):
#     #     if index == "all":
#     #         self._atoms.clear()
#     #         self._molecules.clear()
#     #     elif isinstance(index, int):
#     #         del self._atoms[index]
#     #         del self._molecules[index]
#     #     else:
#     #         print("Error: not clear which set of atoms you want to delete.")
#
#     def _write_output(self, path_output):
#         file_output = open(path_output, "a")
#         file_output.write(self.__str__())
#         file_output.close()
#
#     def generate_input(self, simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#                        bash_script=True, crystals="all", catt=None, matt=None):
#         """
#         Generate the plumed input files. If the catt option is used, only crystals with the specified attribute are
#         used. If the matt option is used only molecules with the specified attributes are used. In both cases,
#         attributes must be specified in the form of a python dict, menaning catt={"AttributeLabel": "AttributeValue"}.
#
#         :param matt: Use Molecular attributes to select the molecules list
#         :param catt: Use crystal attributes to select the crystal list
#         :param simulation: Simulation object
#         :param bash_script: If True, generate a bash script to run simulations
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :return:
#         """
#         if not self._atoms:
#             print("Error: no atoms found. select atoms with the set_atoms module.")
#             exit()
#         print("=" * 100)
#         print(self.__str__())
#
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#
#         for crystal in list_crystals:
#             print(crystal._name)
#             # Select atoms and molecules
#             lines_atoms = []
#             for idx_mol in range(len(self._molecules)):
#                 lines_atoms = generate_atom_list(self._atoms[idx_mol], self._molecules[idx_mol], crystal,
#                                                  keyword="ATOMS", lines=lines_atoms, attributes=matt)
#             file_plumed = open(crystal._path + "plumed_" + self._name + ".dat", "w")
#
#             file_plumed.write("DISTANCE ...\n")
#             for line in lines_atoms:
#                 file_plumed.write(line)
#             file_plumed.write("LABEL=dd_{0}\n"
#                               "COMPONENTS\n"
#                               "... DISTANCE\n\n"
#                               "vv_{0}: NORMALIZE ARG1=dd_{0}.x ARG2=dd_{0}.y ARG3=dd_{0}.z\n"
#                               "dp_mat_{0}: DOTPRODUCT_MATRIX GROUP1=vv_{0}.x GROUP2=vv_{0}.y GROUP3=vv_{0}.z\n"
#                               "ang_mat_{0}: MATHEVAL ARG1=dp_mat_{0} FUNC=acos(x) PERIODIC=NO\n"
#                               "valg_{0}: KDE ARG1=ang_mat_{0} GRID_MIN={1} GRID_MAX={2} "
#                               "GRID_BIN={3} BANDWIDTH={4} KERNEL={5}\n\n"
#                               "PRINT ARG=valg_{0} FILE=plumed_{6}_{0}.dat\n"
#                               "".format(self._name, self._grid_min, self._grid_max,
#                                         self._grid_bins, self._bandwidth, self._kernel, simulation._name))
#             file_plumed.close()
#
#         if bash_script:
#             dt, nsteps, traj_stride, traj_start, traj_end = (None, None, None, None, None)
#
#             file_mdp = open(simulation._path_mdp)
#             for line in file_mdp:
#                 if line.startswith('dt '):
#                     dt = float(line.split()[2])
#                 elif line.startswith(("nstxout", "nstxout-compressed")):
#                     traj_stride = int(line.split()[2])
#                 elif line.startswith('nsteps '):
#                     nsteps = float(line.split()[2])
#             file_mdp.close()
#
#             traj_time = int(nsteps * dt)
#             if traj_time > 0:
#                 if isinstance(self._timeinterval, tuple):
#                     traj_start = self._timeinterval[0]
#                     traj_end = self._timeinterval[1]
#                 elif isinstance(self._timeinterval, int):
#                     traj_start = traj_time - self._timeinterval
#                     traj_end = traj_time
#                 else:
#                     print("Error: No suitable time interval.")
#                     exit()
#
#             file_script = open(simulation._path_data + "/run_plumed_" + self._name + ".sh", "w")
#             file_script.write('#!/bin/bash\n\n'
#                               'crystal_paths="\n')
#             for crystal in list_crystals:
#                 file_script.write(crystal._path + "\n")
#             if isinstance(simulation, Metadynamics):
#                 file_script.write('"\n\n'
#                                   'for crystal in $crystal_paths ; do\n'
#                                   'cd "$crystal" || exit \n'
#                                   '#{0} trjconv -f {1}.xtc -o plumed_{1}.xtc -s {1}.tpr -b {2} -e {3} <<< 0\n'
#                                   '{4} driver --mf_xtc plumed_{1}.xtc --plumed plumed_{5}.dat --timestep {6} '
#                                   '--trajectory-stride {7} --mc mc.dat\n'
#                                   '#rm plumed_{1}.xtc\n'
#                                   'done\n'
#                                   ''.format(simulation._gromacs, simulation._name, traj_start, traj_end,
#                                             self._plumed, self._name, dt, traj_stride))
#             else:
#                 file_script.write('"\n\n'
#                                   'for crystal in $crystal_paths ; do\n'
#                                   'cd "$crystal" || exit \n'
#                                   '{0} trjconv -f {1}.xtc -o plumed_{1}.xtc -s {1}.tpr -b {2} -e {3} <<< 0\n'
#                                   '{4} driver --mf_xtc plumed_{1}.xtc --plumed plumed_{5}.dat --timestep {6} '
#                                   '--trajectory-stride {7} --mc mc.dat\n'
#                                   'rm plumed_{1}.xtc\n'
#                                   'done\n'
#                                   ''.format(simulation._gromacs, simulation._name, traj_start, traj_end,
#                                             self._plumed, self._name, dt, traj_stride))
#             file_script.close()
#         print("=" * 100)
#
#     @staticmethod
#     def get_from_file(path, name):
#         cv = np.genfromtxt(path, skip_header=2)[:, 1:]
#         if np.isnan(cv).any():
#             cv = np.nanmean(cv, axis=0)
#             if np.isnan(cv).any():
#                 print(f"\nError: NaN values present in final distribution of crystal {name}. Check {path} ")
#                 exit()
#             print("\nWarning: NaN values present in some frames of crystal {0._name}. Check {0._path} ")
#         else:
#             cv = np.average(cv, axis=0)
#
#     def get_results(self,
#                     simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#                     crystals: Union[str, list, tuple] = "all",
#                     plot: bool = True, catt=None):
#         """
#         Verify if the distribution has been correctly generated and store the result. If the distribution is taken over
#         different frames, the average is calculated.
#         :param simulation: Simulation object
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :param plot: If true, generate a plot of the distribution.
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#         print("\n" + str(self._name))
#         bar = progressbar.ProgressBar(maxval=len(list_crystals)).start()
#         nbar = 1
#         for crystal in list_crystals:
#             path_output = crystal._path + "plumed_{}_{}.dat".format(simulation._name, self._name)
#             if os.path.exists(path_output):
#                 cv = np.genfromtxt(path_output, skip_header=2)[:, 1:]
#                 if np.isnan(cv).any():
#                     cv = np.nanmean(cv, axis=0)
#                     if np.isnan(cv).any():
#                         print("\nError: NaN values present in final distribution of crystal {0._name}. Check {0._path} "
#                               "".format(crystal))
#                         exit()
#                     print("\nWarning: NaN values present in some frames of crystal {0._name}. Check {0._path} "
#                           "".format(crystal))
#                 else:
#                     cv = np.average(cv, axis=0)
#                 crystal._cvs[self._name] = cv
#                 # Save output and plot distribution
#                 x = np.linspace(self._grid_min, self._grid_max, len(cv))
#                 np.savetxt(crystal._path + "plumed_{}_{}_data.dat".format(simulation._name, self._name),
#                            np.column_stack((x, cv)), fmt=("%1.3f", "%1.5f"),
#                            header="Angle ProbabilityDensity")
#                 if plot:
#                     plt.plot(x, crystal._cvs[self._name], "-")
#                     plt.xlabel("Intermolecular Angle / rad")
#                     plt.xlim(self._grid_min, self._grid_max)
#                     plt.ylabel("Probability Density")
#                     plt.savefig(crystal._path + "plumed_{}_{}_plot.png".format(simulation._name, self._name), dpi=300)
#                     plt.close("all")
#
#                 bar.update(nbar)
#                 nbar += 1
#             else:
#                 print("An error has occurred with Plumed. Check file {} in folder {}."
#                       "".format(path_output, crystal._path))
#
#         bar.finish()
#
#     def identify_orientational_disorder(self,
#                                         simulation: Union[EnergyMinimization, CellRelaxation,
#                                                           MolecularDynamics, Metadynamics],
#                                         crystals: Union[str, list, tuple] = "all",
#                                         cutoff: float = 0.1, catt=None):
#         """
#         Given the intermolecular angle distribution obtained for each crystal in a simulation, it compares
#         it with an homogeneous distribution (typical of melted systems) to identify possible orientational disorder.
#         :param simulation: Simulation object
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :param cutoff: Distance cutoff from melted to be used for identifying melted structures
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#         if self._grid_min != 0. and self._grid_max != np.pi:
#             print("Error: A range between 0 and pi must be used to identify melted structures.")
#             exit()
#         include_melted = False
#         if crystals == "all":
#             include_melted = True
#
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt, _include_melted=include_melted)
#
#         file_hd = open("{}/HD_{}.dat".format(simulation._path_output, simulation._name), "w")
#         file_hd.write("# Tolerance = {}\n#\n# Structures HD\n".format(round(cutoff, 5)))
#         ref = np.sin(np.linspace(0., np.pi, self._grid_bins + 1))
#         for crystal in list_crystals:
#             if not (self._name in crystal._cvs):
#                 print("Error: A distribution for this simulation has not been generated.\n"
#                       "Remember to run the check_normal_termination after running plumed.")
#                 exit()
#             hd = hellinger(crystal._cvs[self._name], ref)
#             file_hd.write("{:35} {:3.3f}\n".format(crystal._name, hd))
#             if hd < cutoff:
#                 crystal._state = "melted"
#         file_hd.close()
#
#
# class Combine(object):
#     """
#     Combine torsional or intermolecular torsional angles in multidimensional distributions.
#
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - clustering_type: How is it treated by clustering algorithms.
#     - kernel: kernel function to use in the histogram generation.
#     - timeinterval: Simulation time interval to generate the distribution.
#     - cvs: List CVs names
#
#     Methods:\n
#     - help(): Print attributes and methods
#     - generate_input(simulation, bash_script=True): Generate the plumed input files
#     - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#     """
#
#     def __init__(self, name: str, cvs: iter):
#         """
#         Combine torsional or intertorsional angles in multidimensional distributions.\n
#         :param name: CV name
#         :param cvs: list of 1-D CVs objects
#         """
#         self._name = name
#         self._cvs = cvs
#
#         self._type = "{} ({}D)".format(cvs[0]._type, len(cvs))
#         self._clustering_type = "distribution"
#         self._plumed = cvs[0]._plumed
#
#         self._kernel = cvs[0]._kernel
#         self._timeinterval = cvs[0]._timeinterval
#
#         # CVs properties
#         self._grid_min = []
#         self._grid_max = []
#         self._grid_bins = []
#         self._bandwidth = []
#         for cv in self._cvs:
#             self._grid_min.append(cv._grid_min)
#             self._grid_max.append(cv._grid_max)
#             self._grid_bins.append(cv._grid_bins)
#             self._bandwidth.append(cv._bandwidth)
#
#     @property
#     def kernel(self):
#         return self._kernel
#
#     @kernel.setter
#     def kernel(self, kernel: str):
#         if kernel.upper() in ("GAUSSIAN", "TRIANGULAR"):
#             self._kernel = kernel
#         else:
#             print("Kernel function not recognized. Choose between 'GAUSSIAN' and 'TRIANGULAR'.")
#
#     @property
#     def timeinterval(self):
#         return self._timeinterval
#
#     @timeinterval.setter
#     def timeinterval(self, time: float, time2: float = None):
#         if time2:
#             self._timeinterval = (time, time2)
#         else:
#             self._timeinterval = time
#
#     # Read-only properties
#     @property
#     def type(self):
#         return self._type
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def clustering_type(self):
#         return self._clustering_type
#
#     @property
#     def cvs(self):
#         txt = "CVs:\n"
#         for cv in self._cvs:
#             txt += cv._name + "\n"
#         return txt
#
#     def __str__(self):
#         txt = ""
#         idx_cv = 0
#         grid_min, grid_max, grid_bins, bandwidth, args = ("", "", "", "", "")
#         txt += "\nCV: {} ({})\n".format(self._name, self._type)
#         for cv in self._cvs:
#             txt += "CV{}: {} ({})\n".format(idx_cv, cv._name, cv._type)
#             grid_min += "{:.3f},".format(cv._grid_min)
#             grid_max += "{:.3f},".format(cv._grid_max)
#             grid_bins += "{},".format(cv._grid_bins)
#             bandwidth += "{:.3f},".format(cv._bandwidth)
#             idx_cv += 1
#
#         txt += "Clustering type: {5}-D Distribution\n" \
#                "Parameters: KERNEL={0} NBINS={1} BANDWIDTH={2} UPPER={3} LOWER={4}\n" \
#                "".format(self._kernel, grid_bins, bandwidth, grid_max, grid_min, len(self._cvs))
#         return txt
#
#     def _write_output(self, path_output):
#         file_output = open(path_output, "a")
#         file_output.write(self.__str__())
#         file_output.close()
#
#     @staticmethod
#     def help():
#         return """
# Combine torsional or intertorsional angles in multidimensional distributions.
#
# Attributes:\n
# - name: name of the CV.
# - type: Type of the CV.
# - clustering_type: How is it treated by clustering algorithms.
# - kernel: kernel function to use in the histogram generation.
# - timeinterval: Simulation time interval to generate the distribution.
# - cvs: List CVs names
#
# Methods:\n
# - help(): Print attributes and methods
# - generate_input(simulation, bash_script=True): Generate the plumed input files
# - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#
# Examples:
# - Create plumed inputs:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# mo = gaff.get_cv("mo")                                        # Retrieve the CV Object
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# mo.generate_input(npt)                                        # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project
#
# - Import distributions once the plumed driver analysis is finished:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# mo = gaff.get_cv("mo")                                        # Retrieve the CV Object
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# mo.get_results(npt, plot=False)                               # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project"""
#
#     def generate_input(self,
#                        simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#                        bash_script: bool = True,
#                        crystals="all",
#                        catt=None, matt=None):
#         """
#         Generate the plumed input files. If the catt option is used, only crystals with the specified attribute are
#         used. If the matt option is used only molecules with the specified attributes are used. In both cases,
#         attributes must be specified in the form of a python dict, menaning catt={"AttributeLabel": "AttributeValue"}.
#
#         :param simulation: Simulation object
#         :param bash_script: If True, generate a bash script to run simulations
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :param matt: Use Molecular attributes to select the molecules list
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#
#         idx_cv = 0
#         list_bins = list()
#         grid_min, grid_max, grid_bins, bandwidth, args = ("", "", "", "", "")
#         print("=" * 100)
#         print(self.__str__())
#         print("Generate plumed input files")
#         for cv in self._cvs:
#             if not cv._atoms:
#                 print("Error: no atoms found in CV {}. select atoms with the set_atoms module.".format(cv._name))
#                 exit()
#
#             grid_min += "{:.3f},".format(cv.grid_min)
#             grid_max += "{:.3f},".format(cv.grid_max)
#             grid_bins += "{},".format(cv.grid_bins)
#             if self._type.startswith("Molecular Orientation"):
#                 list_bins.append(int(cv.grid_bins + 1))
#             elif self._type.startswith("Torsional Angle"):
#                 list_bins.append(int(cv.grid_bins))
#             bandwidth += "{:.3f},".format(cv.bandwidth)
#             if self._type.startswith("Molecular Orientation"):
#                 args += "ARG{}=ang_mat_{} ".format(idx_cv + 1, cv._name)
#             elif self._type.startswith("Torsional Angle"):
#                 args += "ARG{}={} ".format(idx_cv + 1, cv._name)
#
#             idx_cv += 1
#             print("\n")
#
#         self._grid_bins = tuple(list_bins)
#
#         if self._type.startswith("Molecular Orientation"):
#             for crystal in list_crystals:
#                 print(crystal._name)
#                 file_plumed = open(crystal._path + "plumed_" + self._name + ".dat", "w")
#                 for cv in self._cvs:
#                     # Select atoms and molecules
#                     lines_atoms = []
#                     for idx_mol in range(len(cv._molecules)):
#                         lines_atoms = generate_atom_list(cv._atoms[idx_mol], cv._molecules[idx_mol], crystal,
#                                                          keyword="ATOMS", lines=lines_atoms, attributes=matt)
#
#                     file_plumed.write("DISTANCE ...\n")
#                     for line in lines_atoms:
#                         file_plumed.write(line)
#                     file_plumed.write("LABEL=dd_{0}\n"
#                                       "COMPONENTS\n"
#                                       "... DISTANCE\n\n"
#                                       "vv_{0}: NORMALIZE ARG1=dd_{0}.x ARG2=dd_{0}.y ARG3=dd_{0}.z\n"
#                                       "dp_mat_{0}: DOTPRODUCT_MATRIX GROUP1=vv_{0}.x GROUP2=vv_{0}.y GROUP3=vv_{0}.z\n"
#                                       "ang_mat_{0}: MATHEVAL ARG1=dp_mat_{0} FUNC=acos(x) PERIODIC=NO\n\n"
#                                       "".format(cv._name))
#
#                 file_plumed.write("valg_{0}: KDE {7} GRID_MIN={1} GRID_MAX={2} "
#                                   "GRID_BIN={3} BANDWIDTH={4} KERNEL={5}\n\n"
#                                   "PRINT ARG=valg_{0} FILE=plumed_{6}_{0}.dat\n"
#                                   "".format(self._name, grid_min, grid_max,
#                                             grid_bins, bandwidth, self._kernel, simulation._name, args))
#                 file_plumed.close()
#
#         if self._type.startswith("Torsional Angle"):
#             for crystal in list_crystals:
#                 print(crystal._name)
#                 file_plumed = open(crystal._path + "plumed_" + self._name + ".dat", "w")
#                 for cv in self._cvs:
#                     # Select atoms and molecules
#                     lines_atoms = generate_atom_list(cv._atoms, cv.molecule, crystal, keyword="ATOMS", lines=[],
#                                                      attributes=matt)
#
#                     file_plumed.write("TORSIONS ...\n")
#                     for line in lines_atoms:
#                         file_plumed.write(line)
#
#                     file_plumed.write("LABEL={0}\n... TORSIONS\n\n".format(cv._name))
#                 file_plumed.write("kde_{0}: KDE {7} GRID_MIN={1} GRID_MAX={2} "
#                                   "GRID_BIN={3} BANDWIDTH={4} KERNEL={5}\n\n"
#                                   "PRINT ARG=kde_{0} FILE=plumed_{6}_{0}.dat\n"
#                                   "".format(self._name, grid_min, grid_max,
#                                             grid_bins, bandwidth, self._kernel, simulation._name, args))
#                 file_plumed.close()
#
#         if bash_script:
#             dt, nsteps, traj_stride, traj_start, traj_end = (None, None, None, None, None)
#
#             file_mdp = open(simulation._path_mdp)
#             for line in file_mdp:
#                 if line.startswith('dt '):
#                     dt = float(line.split()[2])
#                 elif line.startswith(("nstxout", "nstxout-compressed")):
#                     traj_stride = int(line.split()[2])
#                 elif line.startswith('nsteps '):
#                     nsteps = float(line.split()[2])
#             file_mdp.close()
#
#             traj_time = int(nsteps * dt)
#             if traj_time > 0:
#                 if isinstance(self._timeinterval, tuple):
#                     traj_start = self._timeinterval[0]
#                     traj_end = self._timeinterval[1]
#                 elif isinstance(self._timeinterval, int):
#                     traj_start = traj_time - self._timeinterval
#                     traj_end = traj_time
#                 else:
#                     print("Error: No suitable time interval.")
#                     exit()
#
#             file_script = open(simulation._path_data + "/run_plumed_" + self._name + ".sh", "w")
#             file_script.write('#!/bin/bash\n\n'
#                               'crystal_paths="\n')
#             for crystal in list_crystals:
#                 file_script.write(crystal._path + "\n")
#             if isinstance(simulation, Metadynamics):
#                 file_script.write('"\n\n'
#                                   'for crystal in $crystal_paths ; do\n'
#                                   'cd "$crystal" || exit \n'
#                                   '#{0} trjconv -f {1}.xtc -o plumed_{1}.xtc -s {1}.tpr -b {2} -e {3} <<< 0\n'
#                                   '{4} driver --mf_xtc plumed_{1}.xtc --plumed plumed_{5}.dat --timestep {6} '
#                                   '--trajectory-stride {7} --mc mc.dat\n'
#                                   '#rm plumed_{1}.xtc\n'
#                                   'done\n'
#                                   ''.format(simulation._gromacs, simulation._name, traj_start, traj_end,
#                                             self._plumed, self._name, dt, traj_stride))
#             else:
#                 file_script.write('"\n\n'
#                                   'for crystal in $crystal_paths ; do\n'
#                                   'cd "$crystal" || exit \n'
#                                   '{0} trjconv -f {1}.xtc -o plumed_{1}.xtc -s {1}.tpr -b {2} -e {3} <<< 0\n'
#                                   '{4} driver --mf_xtc plumed_{1}.xtc --plumed plumed_{5}.dat --timestep {6} '
#                                   '--trajectory-stride {7} --mc mc.dat\n'
#                                   'rm plumed_{1}.xtc\n'
#                                   'done\n'
#                                   ''.format(simulation._gromacs, simulation._name, traj_start, traj_end,
#                                             self._plumed, self._name, dt, traj_stride))
#             file_script.close()
#
#         print("=" * 100)
#
#     def get_results(self,
#                     simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#                     crystals: Union[str, list, tuple] = "all",
#                     plot: bool = True,
#                     catt=None):
#         """
#         Verify if the distribution has been correctly generated and store the result. If the distribution is taken over
#         different frames, the average is calculated.
#         :param simulation: Simulation object
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :param plot: If true, generate a plot of the distribution. This is not available for 3D distributions or higher.
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#         print("\n" + str(self._name))
#         bar = progressbar.ProgressBar(maxval=len(list_crystals)).start()
#         nbar = 1
#         for crystal in list_crystals:
#             path_output = crystal._path + "plumed_{}_{}.dat".format(simulation._name, self._name)
#             if os.path.exists(path_output):
#                 cv_dist = np.genfromtxt(path_output, skip_header=1)[:, 1:]
#                 if np.isnan(cv_dist).any():
#                     cv_dist = np.nanmean(cv_dist, axis=0)
#                     if np.isnan(cv_dist).any():
#                         print("\nError: NaN values present in final distribution of crystal {0._name}. Check {0._path} "
#                               "".format(crystal))
#                         exit()
#                     print("\nWarning: NaN values present in some frames of crystal {0._name}. Check {0._path} "
#                           "".format(crystal))
#                 else:
#                     cv_dist = np.average(cv_dist, axis=0)
#                 crystal._cvs[self._name] = cv_dist.reshape(self._grid_bins)
#                 if len(self._cvs) == 2:
#                     # Save output and plot distribution
#                     np.savetxt(crystal._path + "plumed_{}_{}_data.dat".format(simulation._name, self._name),
#                                crystal._cvs[self._name],
#                                header="Probability Density Grid.")
#                     if plot:
#                         extent = self._cvs[0].grid_min, self._cvs[0].grid_max, \
#                                  self._cvs[1].grid_min, self._cvs[1].grid_max
#
#                         plt.imshow(crystal._cvs[self._name], interpolation="nearest", cmap="viridis", extent=extent)
#                         plt.xlabel("{} / rad".format(self._cvs[0]._name))
#                         plt.ylabel("{} / rad".format(self._cvs[1]._name))
#                         plt.savefig(crystal._path + "plumed_{}_{}_plot.png".format(simulation._name, self._name),
#                                     dpi=300)
#                         plt.close("all")
#                 else:
#                     # TODO
#                     pass
#
#                 bar.update(nbar)
#                 nbar += 1
#             else:
#                 print("An error has occurred with Plumed. Check file {} in folder {}."
#                       "".format(path_output, crystal._path))
#         bar.finish()
#
#
# class Planes(_CollectiveVariable):
#     """
#     TODO Change docstrings of everything!!!
#     Generates a distribution of the torsional angles of the selected atoms.
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - plumed: Command line for plumed.
#     - clustering_type: How is it treated by clustering algorithms.
#     - kernel: kernel function to use in the histogram generation.
#     - bandwidth: the bandwidths for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_max: the upper bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     - timeinterval: Simulation time interval to generate the distribution.
#     - atoms: the 4 atom index of the molecular forcefield object used to generate the set of torsional angles
#     - molecule: the molecular forcefield object from which atoms are selected
#
#     Methods:\n
#     - help(): Print attributes and methods
#     - set_atoms(atoms, molecule): Select the 4 atom index from the Molecule obj to generate the set of torsional angles
#     - generate_input(simulation, bash_script=True): Generate the plumed input files
#     - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#     """
#
#     def __init__(self, name: str, plumed: str):
#         """
#         Generates a distribution of the torsional angles of the selected atoms.
#         :param name: str, name of the collective variable. Default output and variables will have this name.
#         :param plumed: command line for the plumed file.
#         """
#         super().__init__(name=name,
#                          cv_type="Planes",
#                          plumed=plumed,
#                          clustering_type="distribution",
#                          kernel="TRIANGULAR",
#                          bandwidth=0.25,
#                          grid_bins=73,
#                          grid_min=-np.pi,
#                          grid_max=np.pi,
#                          grid_space=2 * np.pi / 73,
#                          timeinterval=200)
#
#         self._atoms = list()
#         self._molecule = None
#
#         self._r_0 = 0.1
#         self._d_0 = 2.0
#         self._d_max = 2.5
#         self._normalization = "false"
#
#     @property
#     def atoms(self):
#         return self._atoms
#
#     @atoms.setter
#     def atoms(self, atoms):
#         if len(atoms) == 4:
#             self._atoms = atoms
#         else:
#             print("Error: Planes needs 4 atoms as input")
#
#     @property
#     def molecule(self):
#         return self._molecule
#
#     @molecule.setter
#     def molecule(self, molecule):
#         self._molecule = molecule
#
#     @staticmethod
#     def help():
#         # TODO Modify from torsions to planes
#         return """
# Calculate the distribution of a set of torsional angles.
# It creates the inputs for plumed and stores the results.
#
# Attributes:
# - name: name of the CV.
# - type: Type of the CV (Torsional Angle).
# - plumed: Command line for plumed.
# - clustering_type: How is it treated by clustering algorithms (distribution).
# - kernel: kernel function to use in the histogram generation. It can be "TRIANGULAR" or "GAUSSIAN"
# - bandwidth: the bandwidths for kernel density estimation. The bin size must be smaller than half the bandwidth.
# - grid_min: the lower bounds for the grid.
# - grid_max: the upper bounds for the grid.
# - grid_bins: the number of bins for the grid.
# - grid_space: the approximate grid spacing for the grid.
# - timeinterval: Simulation time interval to generate the distribution.
#                 If a single value is given, t, frames corresponding to the last "t" picoseconds are used.
#                 If two values are given, t1 and t2, frames from time t1 to time t2 are used.
# - atoms: the 4 atom index of the molecular forcefield object used to generate the set of torsional angles.
#                 The same torsional angle in each molecule of the crystal will be considered for the distribution.
# - molecule: the molecular forcefield object from which atoms are selected.
#
# Methods:
# - help(): Print attributes and methods
# - set_atoms(atoms, molecule): Select the 4 atom index from the Molecule obj to generate the set of torsional angles.
#                 The atom index in PyPol starts from 0 and can be seen in the
# - generate_input(simulation, bash_script=True): Generate the plumed input files
# - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#                 If crystal="all", results are stored for all crystals. Alternatively, you can select a subset of
#                 crystals by specifying their IDs in an iterable object.
#                 If plot=True, a plot of the distribution is created. This could be slow for large sets.
#
# Examples:
# - Select atoms of the torsional angles and create plumed inputs:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# tor = gaff.get_cv("tor")                                      # Retrieve the CV Object
# tor.set_atoms((0, 1, 2, 3), molecule)                         # Use the first four atoms to define the torsional angle
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# tor.generate_input(npt)                                       # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project
#
# - Import distributions once the plumed driver analysis is finished:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# tor = gaff.get_cv("tor")                                      # Retrieve the CV Object
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# tor.get_results(npt, plot=False)                              # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project"""
#
#     def set_atoms(self, atoms: Union[list, tuple], molecule: Molecule):
#         """
#         Select atom indices of the reference molecule. This is used to identify the torsions of each molecule in the
#         crystal.
#         :param atoms: list, Atom indices. All atoms indices are available in the project output file after the topology
#         is defined.
#         :param molecule: obj, Reference molecule
#         :return:
#         """
#         self.atoms = atoms
#         self.molecule = molecule
#
#     def generate_input(self,
#                        simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#                        bash_script=True,
#                        crystals="all",
#                        catt=None,
#                        matt=None):
#         """
#         Generate the plumed input files. If the catt option is used, only crystals with the specified attribute are
#         used. If the matt option is used only molecules with the specified attributes are used. In both cases,
#         attributes must be specified in the form of a python dict, menaning catt={"AttributeLabel": "AttributeValue"}.
#
#         :param simulation: Simulation object
#         :param bash_script: If True, generate a bash script to run simulations
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :param matt: Use Molecular attributes to select the molecules list
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#
#         if not self._atoms:
#             print("Error: no atoms found. select atoms with the set_atoms module.")
#             exit()
#         print("=" * 100)
#         print(self.__str__())
#
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#
#         for crystal in list_crystals:
#             print(crystal._name)
#             lines_atoms = generate_atom_list(self._atoms, self._molecule, crystal, keyword="MOL", lines=[],
#                                              attributes=matt)
#             file_plumed = open(crystal._path + "plumed_" + self._name + ".dat", "w")
#             file_plumed.write("PLANES ...\n")
#             for line in lines_atoms:
#                 file_plumed.write(line)
#
#             file_plumed.write("LABEL=planes_{0._name}\n... PLANES\n\n"
#                               "int_tor_{0._name}: INTERMOLECULARTORSIONS MOLS=planes_{0._name} "
#                               "SWITCH={{RATIONAL R_0={0._r_0} D_0={0._d_0} D_MAX={0._d_max}}}\n"
#                               "hist_{0._name}: HISTOGRAM DATA=int_tor_{0._name} GRID_MIN={0._grid_min:.3f} "
#                               "GRID_MAX={0._grid_max:.3f} BANDWIDTH={0._bandwidth:.3f} "
#                               "GRID_BIN={0._grid_bins} KERNEL={0._kernel} NORMALIZATION={0._normalization}\n"
#                               "DUMPGRID GRID=hist_{0._name} FILE=plumed_{1}_{0._name}.dat\n"
#                               "".format(self, simulation._name))
#             file_plumed.close()
#
#         if bash_script:
#             dt, nsteps, traj_stride, traj_start, traj_end = (None, None, None, None, None)
#
#             file_mdp = open(simulation._path_mdp)
#             for line in file_mdp:
#                 if line.startswith('dt '):
#                     dt = float(line.split()[2])
#                 elif line.startswith(("nstxout", "nstxout-compressed")):
#                     traj_stride = int(line.split()[2])
#                 elif line.startswith('nsteps '):
#                     nsteps = float(line.split()[2])
#             file_mdp.close()
#
#             traj_time = int(nsteps * dt)
#             if traj_time > 0:
#                 if isinstance(self._timeinterval, tuple):
#                     traj_start = self._timeinterval[0]
#                     traj_end = self._timeinterval[1]
#                 elif isinstance(self._timeinterval, int):
#                     traj_start = traj_time - self._timeinterval
#                     traj_end = traj_time
#                 else:
#                     print("Error: No suitable time interval.")
#                     exit()
#
#             file_script = open(simulation._path_data + "/run_plumed_" + self._name + ".sh", "w")
#             file_script.write('#!/bin/bash\n\n'
#                               'crystal_paths="\n')
#             for crystal in list_crystals:
#                 file_script.write(crystal._path + "\n")
#
#             if isinstance(simulation, Metadynamics):
#                 file_script.write('"\n\n'
#                                   'for crystal in $crystal_paths ; do\n'
#                                   'cd "$crystal" || exit \n'
#                                   '#{0} trjconv -f {1}.xtc -o plumed_{1}.xtc -s {1}.tpr -b {2} -e {3} <<< 0\n'
#                                   '{4} driver --mf_xtc plumed_{1}.xtc --plumed plumed_{5}.dat --timestep {6} '
#                                   '--trajectory-stride {7} --mc mc.dat\n'
#                                   '#rm plumed_{1}.xtc\n'
#                                   'done\n'
#                                   ''.format(simulation._gromacs, simulation._name, traj_start, traj_end,
#                                             self._plumed, self._name, dt, traj_stride))
#                 file_script.close()
#             else:
#                 file_script.write('"\n\n'
#                                   'for crystal in $crystal_paths ; do\n'
#                                   'cd "$crystal" || exit \n'
#                                   '{0} trjconv -f {1}.xtc -o plumed_{1}.xtc -s {1}.tpr -b {2} -e {3} <<< 0\n'
#                                   '{4} driver --mf_xtc plumed_{1}.xtc --plumed plumed_{5}.dat --timestep {6} '
#                                   '--trajectory-stride {7} --mc mc.dat\n'
#                                   'rm plumed_{1}.xtc\n'
#                                   'done\n'
#                                   ''.format(simulation._gromacs, simulation._name, traj_start, traj_end,
#                                             self._plumed, self._name, dt, traj_stride))
#                 file_script.close()
#         print("=" * 100)
#
#     def get_results(self,
#                     simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#                     crystals: Union[str, list, tuple] = "all",
#                     plot: bool = True, catt=None):
#         """
#         Verify if the distribution has been correctly generated and store the result. If the distribution is taken over
#         different frames, the average is calculated.
#         :param simulation: Simulation object
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :param plot: If true, generate a plot of the distribution.
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#         print("\n" + str(self._name))
#         bar = progressbar.ProgressBar(maxval=len(list_crystals)).start()
#         nbar = 1
#         for crystal in list_crystals:
#             path_plumed_output = crystal._path + "plumed_{}_{}.dat".format(simulation._name, self._name)
#             if os.path.exists(path_plumed_output):
#                 cv = np.genfromtxt(path_plumed_output, skip_header=1)[:, 1]
#                 cv /= cv.sum()
#                 crystal._cvs[self._name] = cv
#                 # Save output and plot distribution
#                 x = np.linspace(self._grid_min, self._grid_max, len(cv))
#                 np.savetxt(crystal._path + "plumed_{}_{}_data.dat".format(simulation._name, self._name),
#                            np.column_stack((x, cv)), fmt=("%1.3f", "%1.5f"),
#                            header="Angle ProbabilityDensity")
#                 if plot:
#                     plt.plot(x, crystal._cvs[self._name], "-")
#                     plt.xlabel("Intermolecular Angle / rad")
#                     plt.xlim(self._grid_min, self._grid_max)
#                     plt.ylabel("Probability Density")
#                     plt.savefig(crystal._path + "plumed_{}_{}_plot.png".format(simulation._name, self._name), dpi=300)
#                     plt.close("all")
#                 bar.update(nbar)
#                 nbar += 1
#             else:
#                 print("An error has occurred with Plumed. Check file {} in folder {}."
#                       "".format(path_plumed_output, crystal._path))
#         bar.finish()
#
#     def __str__(self):
#         txt = super(Planes, self).__str__()
#         if self._atoms:
#             txt += "\nAtoms:  "
#             for atom in self._atoms:
#                 txt += "{}({})  ".format(atom, self._molecule._atoms[atom]._label)
#         else:
#             txt += "No atoms found in CV {}. Select atoms with the 'set_atoms' module.\n".format(self._name)
#         txt += "\n"
#         return txt
#
#     def _write_output(self, path_output):
#         file_output = open(path_output, "a")
#         file_output.write(self.__str__())
#         file_output.close()
#
#
# class RDF(_CollectiveVariable):
#     """
#     Generates a distribution of the intermolecular torsional angles of the selected atoms.
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - plumed: Command line for plumed.
#     - clustering_type: How is it treated by clustering algorithms.
#     - kernel: kernel function to use in the histogram generation.
#     - bandwidth: the bandwidths for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     - timeinterval: Simulation time interval to generate the distribution.
#     - atoms: the atoms index of the molecular forcefield object used to calculate molecule position
#     - molecules: the molecular forcefield object from which atoms are selected
#     - center: Calculate the molecule position based on geometrical center or center of mass
#     - r_0: R_0 parameter
#
#     Methods:\n
#     - help(): Print attributes and methods
#     - set_atoms(atoms, molecule): Select the atoms from the Molecule obj to generate calculate the molecule position
#     - generate_input(simulation, bash_script=True): Generate the plumed input files
#     - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#     """
#
#     def __init__(self, name, plumed, center="geometrical"):
#         """
#
#         :param name:
#         :param center:
#         """
#         super().__init__(name=name,
#                          cv_type="Radial Distribution Function",
#                          plumed=plumed,
#                          clustering_type="distribution",
#                          kernel="TRIANGULAR",
#                          grid_space=0.01,
#                          bandwidth=0.01,
#                          timeinterval=200)
#
#         self._center = center
#         self._atoms = list()
#         self._molecules = list()
#
#         self._switching_function = "RATIONAL"
#         self._r_0 = 0.01
#
#     # @property
#     # def switching_function(self):
#     #     return self._switching_function
#
#     @property
#     def center(self):
#         return self._center
#
#     @center.setter
#     def center(self, center):
#         if center.lower() in ("com", "geometrical"):
#             self._center = center.lower()
#         else:
#             print("Method to evaluate molecule position, not available, choose between:"
#                   "\n - 'com': Calculate the center of mass of each molecule."
#                   "\n - 'geometrical': Calculate the centroid of each molecule.")
#
#     @property
#     def r_0(self):
#         return self._r_0
#
#     @r_0.setter
#     def r_0(self, r_0=None):
#         if not r_0:
#             self._r_0 = self._grid_space
#         elif r_0 > 0:
#             self._r_0 = r_0
#         else:
#             print("R_0 cannot have values lower than 0.")
#
#     @property
#     def atoms(self):
#         return self._atoms
#
#     @property
#     def molecules(self):
#         return self._molecules
#
#     def __str__(self):
#         txt = super().__str__()
#         if self._atoms:
#             for idx_mol in range(len(self._molecules)):
#                 txt += "\nMolecule '{}': ".format(self._molecules[idx_mol]._residue)
#                 for atom in self._atoms[idx_mol]:
#                     txt += "{}({})  ".format(atom, self._molecules[idx_mol]._atoms[atom]._label)
#                 txt += "\n"
#         else:
#             txt += "No atoms found in CV {}. Select atoms with the 'set_atoms' module.".format(self._name)
#         return txt
#
#     @staticmethod
#     def help():
#         return """
# Calculate the radial distribution function of the molecules
# Attributes:\n
# - name: name of the CV.
# - type: Type of the CV.
# - plumed: Command line for plumed.
# - clustering_type: How is it treated by clustering algorithms.
# - kernel: kernel function to use in the histogram generation.
# - bandwidth: the bandwidths for kernel density estimation.
# - grid_min: the lower bounds for the grid.
# - grid_bins: the number of bins for the grid.
# - grid_space: the approximate grid spacing for the grid.
# - timeinterval: Simulation time interval to generate the distribution.
# - atoms: the atoms index of the molecular forcefield object used to calculate molecule position
# - molecules: the molecular forcefield object from which atoms are selected
# - center: Calculate the molecule position based on geometrical center or center of mass
# - r_0: R_0 parameter
#
# Methods:\n
# - help(): Print attributes and methods
# - set_atoms(atoms="all", molecule): Select the atoms from the Molecule obj to generate calculate the molecule position.
#                 You can use atoms="all" to select all atoms or atoms="non-hydrogen" to select all atoms except H.
# - generate_input(simulation, bash_script=True): Generate the plumed input files for the distribution of distances.
# - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and calculate the
#                 radial distribution function from the distribution of distances.
#
# Examples:\n
# - Generate inputs for the RDF of the centers of mass:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# rdf = gaff.get_cv("rdf")                                      # Retrieve the CV Object
# rdf.center = "com"                                            # Select how to calculate molecules position
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# rdf.set_atoms("all", molecule)                                # Set all the atoms in the molecule
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# rdf.generate_input(npt)                                       # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project
#
# - Generate inputs for the RDF of molecule geometrical center:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# rdf = gaff.get_cv("rdf")                                      # Retrieve the CV Object
# rdf.center = "geometrical"                                    # Select how to calculate molecules position
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# rdf.set_atoms("non-hydrogen", molecule)                       # Select the atoms in the molecule
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# rdf.generate_input(npt)                                       # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project
#
# - Import distributions once the plumed driver analysis is finished:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# rdf = gaff.get_cv("rdf")                                      # Retrieve the CV Object
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# rdf.get_results(npt, plot=False)                              # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project
#     """
#
#     def set_atoms(self, atoms: str, molecule: Molecule, overwrite: bool = True):
#         """
#         Select the atoms from the Molecule obj to generate calculate the molecule position.
#         :param atoms: str. You can use atoms="all" to select all atoms or atoms="non-hydrogen"
#                       to select all atoms except H.
#         :param molecule: Molecular forcfield Molecule object
#         :param overwrite: If True, ignores previous atom settings
#         :return:
#         """
#         for idx_mol in range(len(self._molecules)):
#             ref_mol = self._molecules[idx_mol]
#             if ref_mol._residue == molecule._residue and overwrite:
#                 del self._molecules[idx_mol]
#                 del self._atoms[idx_mol]
#
#         if atoms == "all":
#             atoms = list()
#             for atom in molecule._atoms:
#                 atoms.append(atom._index)
#         elif atoms == "non-hydrogen":
#             atoms = list()
#             for atom in molecule._atoms:
#                 if atom._element.upper() != "H":
#                     atoms.append(atom._index)
#         self._atoms.append(list(atoms))
#         self._molecules.append(molecule)
#
#     def del_atoms(self, index: Union[str, int] = "all"):
#         if index == "all":
#             self._atoms.clear()
#             self._molecules.clear()
#         elif isinstance(index, int):
#             del self._atoms[index]
#             del self._molecules[index]
#         else:
#             print("Error: not clear which set of atoms you want to delete.")
#
#     def _write_output(self, path_output):
#         file_output = open(path_output, "a")
#         file_output.write(self.__str__())
#         file_output.close()
#
#     def generate_input(self,
#                        simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#                        bash_script: bool = True,
#                        crystals="all",
#                        catt=None,
#                        matt=None):
#         """
#         Generate the plumed input files. If the catt option is used, only crystals with the specified attribute are
#         used. If the matt option is used only molecules with the specified attributes are used. In both cases,
#         attributes must be specified in the form of a python dict, menaning catt={"AttributeLabel": "AttributeValue"}.
#
#         :param matt: Use Molecular attributes to select the molecules list
#         :param catt: Use crystal attributes to select the crystal list
#         :param bash_script: If True, generate a bash script to run simulations
#         :param simulation: Simulation object
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :return:
#         """
#
#         if not self._atoms:
#             print("Error: no atoms found. Select atoms with the set_atoms module.")
#             exit()
#
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#
#         print("=" * 100)
#         print("Generate plumed input files")
#         print("CV: {} ({})".format(self._name, self._type))
#         print("Atoms:", end=" ")
#         for idx_mol in range(len(self._molecules)):
#             print("\nMolecule '{}': ".format(self._molecules[idx_mol]._residue))
#             for atom in self._atoms[idx_mol]:
#                 print("{}({})".format(atom, self._molecules[idx_mol]._atoms[atom]._label), end="  ")
#
#         print("\nClustering type: Distribution\n"
#               "Parameters: KERNEL={0} BANDWIDTH={1:.3f} LOWER={2:.3f} BIN_SPACE={3:.3f}"
#               "".format(self._kernel, self._bandwidth, self._r_0, self._grid_space))
#
#         for crystal in list_crystals:
#             print(crystal._name)
#
#             d_max = 0.5 * np.min(np.array([crystal._box[0, 0], crystal._box[1, 1], crystal._box[2, 2]]))
#             nbins = int(round((d_max - self._r_0) / self._grid_space, 0))
#
#             lines_atoms = []
#             for idx_mol in range(len(self._molecules)):
#                 lines_atoms = generate_atom_list(self._atoms[idx_mol], self._molecules[idx_mol], crystal,
#                                                  keyword="ATOMS", lines=lines_atoms, index_lines=False,
#                                                  attributes=matt)
#
#             file_plumed = open(crystal._path + "plumed_" + self._name + ".dat", "w")
#             idx_com = 1
#             str_group = ""
#             if self._center == "geometrical":
#                 for line in lines_atoms:
#                     file_plumed.write("{}_c{}: CENTER {}".format(self._name, idx_com, line))
#                     str_group += "{}_c{},".format(self._name, idx_com)
#                     idx_com += 1
#             elif self._center.upper() == "COM":
#                 for line in lines_atoms:
#                     file_plumed.write("{}_c{}: COM {}".format(self._name, idx_com, line))
#                     str_group += "{}_c{},".format(self._name, idx_com)
#                     idx_com += 1
#
#             str_group = str_group[:-1]
#             file_plumed.write("{0}_g: GROUP ATOMS={1}\n"
#                               "{0}_d: DISTANCES GROUP={0}_g MORE_THAN={{RATIONAL R_0={2} D_0={3} D_MAX={3}}} "
#                               "HISTOGRAM={{{6} NBINS={5} BANDWIDTH={4} UPPER={3} LOWER={2}}}\n"
#                               "PRINT ARG={0}_d.* FILE=plumed_{7}_{0}.dat\n\n"
#                               "".format(self._name, str_group, self._r_0, d_max, self._bandwidth,
#                                         nbins, self._kernel, simulation._name))
#             file_plumed.close()
#
#         if bash_script:
#
#             dt, nsteps, traj_stride, traj_start, traj_end = (None, None, None, None, None)
#
#             file_mdp = open(simulation._path_mdp)
#             for line in file_mdp:
#                 if line.startswith('dt '):
#                     dt = float(line.split()[2])
#                 elif line.startswith(("nstxout", "nstxout-compressed")):
#                     traj_stride = int(line.split()[2])
#                 elif line.startswith('nsteps '):
#                     nsteps = float(line.split()[2])
#             file_mdp.close()
#
#             traj_time = int(nsteps * dt)
#             if traj_time > 0:
#                 if isinstance(self._timeinterval, tuple):
#                     traj_start = self._timeinterval[0]
#                     traj_end = self._timeinterval[1]
#                 elif isinstance(self._timeinterval, int):
#                     traj_start = traj_time - self._timeinterval
#                     traj_end = traj_time
#                 else:
#                     print("Error: No suitable time interval.")
#                     exit()
#
#             file_script = open(simulation._path_data + "/run_plumed_" + self._name + ".sh", "w")
#             file_script.write('#!/bin/bash\n\n'
#                               'crystal_paths="\n')
#             for crystal in list_crystals:
#                 file_script.write(crystal._path + "\n")
#             if isinstance(simulation, Metadynamics):
#                 file_script.write('"\n\n'
#                                   'for crystal in $crystal_paths ; do\n'
#                                   'cd "$crystal" || exit \n'
#                                   '#{0} trjconv -f {1}.xtc -o plumed_{1}.xtc -s {1}.tpr -b {2} -e {3} <<< 0\n'
#                                   '{4} driver --mf_xtc plumed_{1}.xtc --plumed plumed_{5}.dat --timestep {6} '
#                                   '--trajectory-stride {7} --mc mc.dat\n'
#                                   '#rm plumed_{1}.xtc\n'
#                                   'done\n'
#                                   ''.format(simulation._gromacs, simulation._name, traj_start, traj_end,
#                                             self._plumed, self._name, dt, traj_stride))
#             else:
#                 file_script.write('"\n\n'
#                                   'for crystal in $crystal_paths ; do\n'
#                                   'cd "$crystal" || exit \n'
#                                   '{0} trjconv -f {1}.xtc -o plumed_{1}.xtc -s {1}.tpr -b {2} -e {3} <<< 0\n'
#                                   '{4} driver --mf_xtc plumed_{1}.xtc --plumed plumed_{5}.dat --timestep {6} '
#                                   '--trajectory-stride {7} --mc mc.dat\n'
#                                   'rm plumed_{1}.xtc\n'
#                                   'done\n'
#                                   ''.format(simulation._gromacs, simulation._name, traj_start, traj_end,
#                                             self._plumed, self._name, dt, traj_stride))
#             file_script.close()
#
#     def get_results(self,
#                     simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#                     crystals: Union[str, list, tuple] = "all",
#                     plot: bool = True, catt=None):
#         """
#         Verify if the distribution has been correctly generated and store the result. If the distribution is taken over
#         different frames, the average is calculated.
#         :param simulation: Simulation object
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :param plot: If true, generate a plot of the distribution.
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#         print("\n" + str(self._name))
#         bar = progressbar.ProgressBar(maxval=len(list_crystals)).start()
#         nbar = 1
#         for crystal in list_crystals:
#             path_output = crystal._path + "plumed_{}_{}.dat".format(simulation._name, self._name)
#             if os.path.exists(path_output):
#                 dn_r = np.genfromtxt(path_output, skip_header=1)[:, 2:]
#                 if np.isnan(dn_r).any():
#                     dn_r = np.nanmean(dn_r, axis=0)
#                     if np.isnan(dn_r).any():
#                         print("\nError: NaN values present in final distribution of crystal {0._name}. Check {0._path} "
#                               "".format(crystal))
#                         exit()
#                     print("\nWarning: NaN values present in some frames of crystal {0._name}. Check {0._path} "
#                           "".format(crystal))
#                 else:
#                     dn_r = np.average(dn_r, axis=0)
#
#                 d_max = 0.5 * np.min(np.array([crystal._box[0, 0], crystal._box[1, 1], crystal._box[2, 2]]))
#                 nbins = int(round((d_max - self._r_0) / self._grid_space, 0))
#                 r = np.linspace(self._r_0, d_max, nbins)
#                 rho = crystal._Z / crystal._volume
#
#                 cv = np.where(r > 0, dn_r / (4 * np.pi * rho * r ** 2 * self._grid_space) / crystal._Z * 2.0, 0.)
#                 crystal._cvs[self._name] = cv
#                 # Save output and plot distribution
#                 np.savetxt(crystal._path + "plumed_{}_{}_data.dat".format(simulation._name, self._name),
#                            np.column_stack((r, cv)), fmt=("%1.4f", "%1.5f"),
#                            header="r RDF")
#                 if plot:
#                     plt.plot(r, crystal._cvs[self._name], "-")
#                     plt.xlabel("r / nm")
#                     plt.xlim(self._r_0, d_max)
#                     plt.ylabel("Probability Density")
#                     plt.savefig(crystal._path + "plumed_{}_{}_plot.png".format(simulation._name, self._name), dpi=300)
#                     plt.close("all")
#
#                 bar.update(nbar)
#                 nbar += 1
#             else:
#                 print("An error has occurred with Plumed. Check file {} in folder {}."
#                       "".format(path_output, crystal._path))
#         bar.finish()
#
#
# class _OwnDistributions(object):  # TODO Change name to Distributions
#     """
#     General Class for Collective Variables.
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - clustering_type: How is it treated by clustering algorithms.
#     - kernel: kernel function to use in the histogram generation.
#     - bandwidth: the bandwidths for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_max: the upper bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     - timeinterval: Simulation time interval to generate the distribution.
#     """
#
#     def __init__(self, name: str, cv_type: str, clustering_type="distribution", kernel="gaussian",
#                  timeinterval: Union[float, tuple] = None):
#         """
#         General Class for Collective Variables.
#         :param name: name of the CV.
#         :param cv_type: Type of the CV.
#         :param clustering_type: How is it treated by clustering algorithms.
#         :param kernel: kernel function to use in the histogram generation.
#         :param timeinterval: Simulation time interval to generate the distribution.
#         """
#         self._name = name
#         self._type = cv_type
#         self._clustering_type = clustering_type
#
#         self._kernel = kernel
#         self._timeinterval = timeinterval
#
#     @property
#     def kernel(self):
#         return self._kernel
#
#     @kernel.setter
#     def kernel(self, kernel: str):
#         if kernel.lower() in ("gaussian", "tophat", "epanechnikov", "exponential", "linear", "cosine"):
#             self._kernel = kernel
#         else:
#             print('Kernel function not recognized. Available formats from sklearn: "gaussian", "tophat", '
#                   '"epanechnikov", "exponential", "linear", "cosine".')
#
#     @property
#     def timeinterval(self):
#         return self._timeinterval
#
#     @timeinterval.setter
#     def timeinterval(self, time: float, time2: float = None):
#         if time2:
#             self._timeinterval = (time, time2)
#         else:
#             self._timeinterval = time
#
#     # Read-only properties
#     @property
#     def type(self):
#         return self._type
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def clustering_type(self):
#         return self._clustering_type
#
#     def __str__(self):
#         txt = """
# CV: {0._name} ({0._type})
# Clustering Type: {0._clustering_type}""".format(self)
#         return txt
#
#     @staticmethod
#     def _kde_ovect_rvect(ovect, rvect, r_grid_min=0., r_grid_max=4., r_bw=0.05, r_bins=100j,
#                          o_grid_min=0., o_grid_max=np.pi, o_bw=0.05, o_bins=100j, mirror=False):
#         data = []
#         for i in range(207):
#             ax, ay, az = ovect[i, :]
#             for j in range(i + 1, 208):
#                 distance = np.linalg.norm(rvect[i, :] - rvect[j, :])
#                 if distance > r_grid_max:
#                     continue
#                 bx, by, bz = ovect[j, :]
#                 angle = np.arccos(
#                     (ax * bx + ay * by + az * bz) / np.sqrt(
#                         (ax * ax + ay * ay + az * az) * (bx * bx + by * by + bz * bz)))
#
#                 data.append(np.array([angle, distance]))
#
#         data = np.array(data)
#         kde = KDE()
#         data_scaled = data / np.array([o_bw, r_bw])
#         kde.fit(data_scaled)
#         xx, yy = np.mgrid[int(o_grid_min / o_bw):int(o_grid_max / o_bw):o_bins,
#                  int(r_grid_min / r_bw):int(r_grid_max / r_bw): r_bins]
#         zz = np.reshape(np.exp(kde.score_samples(np.vstack([xx.ravel(), yy.ravel()]).T)), xx.shape).T
#         if mirror:
#             zz = (zz + np.flip(zz, axis=1)) / 2.
#
#         return zz
#
#
# class RDFPlanes(_OwnDistributions):
#     """
#     TODO Change docstrings of everything!!!
#     TODO Do equivalent for RDFMO once everything is tested.
#     Generates a distribution of the torsional angles of the selected atoms.
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - plumed: Command line for plumed.
#     - clustering_type: How is it treated by clustering algorithms.
#     - kernel: kernel function to use in the histogram generation.
#     - bandwidth: the bandwidths for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_max: the upper bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     - timeinterval: Simulation time interval to generate the distribution.
#     - atoms: the 4 atom index of the molecular forcefield object used to generate the set of torsional angles
#     - molecule: the molecular forcefield object from which atoms are selected
#
#     Methods:\n
#     - help(): Print attributes and methods
#     - set_atoms(atoms, molecule): Select the 4 atom index from the Molecule obj to generate the set of torsional angles
#     - generate_input(simulation, bash_script=True): Generate the plumed input files
#     - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#     """
#
#     def __init__(self, name: str):
#         """
#         Generates a distribution of the torsional angles of the selected atoms.
#         :param name: str, name of the collective variable. Default output and variables will have this name.
#         """
#         super().__init__(name=name,
#                          cv_type="RDF-Planes",
#                          clustering_type="distribution",
#                          kernel="gaussian",
#                          timeinterval=200)
#
#         self._atoms = list()
#         self._molecule = None
#
#         self._r_grid_min = 0.
#         self._r_grid_max = None
#         self._r_bw = 0.05
#         self._r_bins = 100j
#         self._r_grid_space = 0.01
#         self._o_grid_min = 0.
#         self._o_grid_max = np.pi
#         self._o_bw = 0.05
#         self._o_bins = 100j
#         self._mirror = True
#
#     @property
#     def rdf_grid_min(self):
#         return self._r_grid_min
#
#     @rdf_grid_min.setter
#     def rdf_grid_min(self, value: float):
#         self._r_grid_min = value
#
#     @property
#     def rdf_grid_max(self):
#         return self._r_grid_max
#
#     @rdf_grid_max.setter
#     def rdf_grid_max(self, value: float):
#         self._r_grid_max = value
#
#     @property
#     def rdf_grid_bins(self):
#         return self._r_bins
#
#     @rdf_grid_bins.setter
#     def rdf_grid_bins(self, value: Union[float, int, complex]):
#         if isinstance(value, (float, int)):
#             value = complex(0, value)
#         self._r_bins = value
#
#     @property
#     def rdf_bandwidth(self):
#         return self._r_bw
#
#     @rdf_bandwidth.setter
#     def rdf_bandwidth(self, value: float):
#         self._r_bw = value
#
#     @property
#     def planes_grid_min(self):
#         return self._o_grid_min
#
#     @planes_grid_min.setter
#     def planes_grid_min(self, value: float):
#         self._o_grid_min = value
#
#     @property
#     def planes_grid_max(self):
#         return self._o_grid_max
#
#     @planes_grid_max.setter
#     def planes_grid_max(self, value: float):
#         self._o_grid_max = value
#
#     @property
#     def planes_grid_bins(self):
#         return self._o_bins
#
#     @planes_grid_bins.setter
#     def planes_grid_bins(self, value: Union[float, int, complex]):
#         if isinstance(value, (float, int)):
#             value = complex(0, value)
#         self._o_bins = value
#
#     @property
#     def planes_bandwidth(self):
#         return self._o_bw
#
#     @planes_bandwidth.setter
#     def planes_bandwidth(self, value: float):
#         self._o_bw = value
#
#     @property
#     def atoms(self):
#         return self._atoms
#
#     @atoms.setter
#     def atoms(self, atoms):
#         if len(atoms) == 3:
#             self._atoms = atoms
#         else:
#             print("Error: RDF-Planes needs 3 atoms as input")
#
#     @property
#     def molecule(self):
#         return self._molecule
#
#     @molecule.setter
#     def molecule(self, molecule):
#         self._molecule = molecule
#
#     @staticmethod
#     def help():
#         # TODO Modify from torsions to planes
#         return """
# Calculate the distribution of a set of torsional angles.
# It creates the inputs for plumed and stores the results.
#
# Attributes:
# - name: name of the CV.
# - type: Type of the CV (Torsional Angle).
# - plumed: Command line for plumed.
# - clustering_type: How is it treated by clustering algorithms (distribution).
# - kernel: kernel function to use in the histogram generation. It can be "TRIANGULAR" or "GAUSSIAN"
# - bandwidth: the bandwidths for kernel density estimation. The bin size must be smaller than half the bandwidth.
# - grid_min: the lower bounds for the grid.
# - grid_max: the upper bounds for the grid.
# - grid_bins: the number of bins for the grid.
# - grid_space: the approximate grid spacing for the grid.
# - timeinterval: Simulation time interval to generate the distribution.
#                 If a single value is given, t, frames corresponding to the last "t" picoseconds are used.
#                 If two values are given, t1 and t2, frames from time t1 to time t2 are used.
# - atoms: the 4 atom index of the molecular forcefield object used to generate the set of torsional angles.
#                 The same torsional angle in each molecule of the crystal will be considered for the distribution.
# - molecule: the molecular forcefield object from which atoms are selected.
#
# Methods:
# - help(): Print attributes and methods
# - set_atoms(atoms, molecule): Select the 4 atom index from the Molecule obj to generate the set of torsional angles.
#                 The atom index in PyPol starts from 0 and can be seen in the
# - generate_input(simulation, bash_script=True): Generate the plumed input files
# - get_results(simulation, crystal='all', plot=True): Check if the plumed driver analysis is ended and store results
#                 If crystal="all", results are stored for all crystals. Alternatively, you can select a subset of
#                 crystals by specifying their IDs in an iterable object.
#                 If plot=True, a plot of the distribution is created. This could be slow for large sets.
#
# Examples:
# - Select atoms of the torsional angles and create plumed inputs:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# tor = gaff.get_cv("tor")                                      # Retrieve the CV Object
# tor.set_atoms((0, 1, 2, 3), molecule)                         # Use the first four atoms to define the torsional angle
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# tor.generate_input(npt)                                       # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project
#
# - Import distributions once the plumed driver analysis is finished:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# molecule = gaff.get_molecule("MOL")                           # Use molecular forcefield info for the CV
# tor = gaff.get_cv("tor")                                      # Retrieve the CV Object
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# tor.get_results(npt, plot=False)                              # Generate plumed driver input for the selected simulation
# project.save()                                                # Save project"""
#
#     def set_atoms(self, atoms: Union[list, tuple], molecule: Molecule):
#         """
#         Select atom indices of the reference molecule. This is used to identify the torsions of each molecule in the
#         crystal.
#         :param atoms: list, Atom indices. All atoms indices are available in the project output file after the topology
#         is defined.
#         :param molecule: obj, Reference molecule
#         :return:
#         """
#         self.atoms = atoms
#         self.molecule = molecule
#
#     def run(self,
#             simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#             crystals="all",
#             catt=None,
#             matt=None,
#             mirror=False,
#             plot=True):
#         """
#         Generate the plumed input files. If the catt option is used, only crystals with the specified attribute are
#         used. If the matt option is used only molecules with the specified attributes are used. In both cases,
#         attributes must be specified in the form of a python dict, menaning catt={"AttributeLabel": "AttributeValue"}.
#
#         :param simulation: Simulation object
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :param matt: Use Molecular attributes to select the molecules list
#         :param catt: Use crystal attributes to select the crystal list
#         :param mirror:
#         :param plot: Plot the distribution
#         :return:
#         """
#
#         if not self._atoms:
#             print("Error: no atoms found. select atoms with the set_atoms module.")
#             exit()
#         print("=" * 100)
#         print(self.__str__())
#
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#
#         for crystal in list_crystals:
#             print(crystal._name)
#
#             if matt is None:
#                 matt = {}
#
#             mols = []
#             for mol in crystal._load_coordinates():
#                 if self._molecule._residue == mol._residue:
#                     if matt:
#                         if matt.items() <= mol._attributes.items():
#                             mols.append(mol._index)
#                     else:
#                         mols.append(mol._index)
#
#             if self._r_grid_max:
#                 crystal_grid_max = self._r_grid_max
#                 crystal_grid_bins = self._r_bins
#             else:
#                 crystal_grid_max = 0.5 * np.min(np.array([crystal._box[0, 0], crystal._box[1, 1], crystal._box[2, 2]]))
#                 crystal_grid_bins = complex(0,
#                                             int(round((crystal_grid_max - self._r_grid_min) / self._r_grid_space, 0)))
#
#             file_ndx = open(crystal._path + f"/PYPOL_TMP_{simulation._name}.ndx")
#             file_ndx.write("[ System ] \n")
#             for mol in mols:
#                 for atom in self._atoms:
#                     file_ndx.write("{:5} ".format(atom + mol * self._molecule._natoms + 1))
#             file_ndx.close()
#
#             traj_start, traj_end = (None, None)
#             traj_time = float(simulation._mdp["dt"]) * float(simulation._mdp["nsteps"])
#             if isinstance(self._timeinterval, tuple):
#                 traj_start = self._timeinterval[0]
#                 traj_end = self._timeinterval[1]
#             elif isinstance(self._timeinterval, int):
#                 traj_start = traj_time - self._timeinterval
#                 traj_end = traj_time
#             else:
#                 print("Error: No suitable time interval.")
#                 exit()
#             os.chdir(crystal._path)
#             os.system('{0} trjconv -f {1}.xtc -o PYPOL_TMP_{1}.gro -n PYPOL_TMP_{1}.ndx -s {1}.tpr -b {2} -e {3} <<< '
#                       '0\n '.format(simulation._gromacs, simulation._name, traj_start, traj_end))
#
#             planes = {}
#             r_plane = {}
#             file_gro = open(crystal._path + f"/PYPOL_TMP_{simulation._name}.gro")
#             frame, plane = 0, 0
#             for line in file_gro:
#                 if "t=" in line:
#                     frame = line.split()[-1]
#                     planes[frame] = np.zeros((len(mols), 3))
#                     r_plane[frame] = np.zeros((len(mols), 3))
#                     plane = 0
#                     next(file_gro)
#                 elif line[5:8] == self._molecule._residue:
#                     a1 = np.array([float(line[23:28]), float(line[31:36]), float(line[39:44])])
#                     line = next(file_gro)
#                     a2 = np.array([float(line[23:28]), float(line[31:36]), float(line[39:44])])
#                     line = next(file_gro)
#                     a3 = np.array([float(line[23:28]), float(line[31:36]), float(line[39:44])])
#                     planes[frame][plane, :] = np.cross(a2 - a1, a2 - a3)
#                     r_plane[frame][plane, :] = np.mean([a1, a2, a3], axis=0)
#                     plane += 1
#             file_gro.close()
#             data = np.zeros((int(len(mols) * (len(mols) - 1) / 2), 2))
#             d = 0
#             for frame in planes.keys():
#                 for i in range(len(mols) - 1):
#                     ax, ay, az = planes[frame][i, :]
#                     r_i = r_plane[frame][i, :]
#                     for j in range(i + 1, len(mols)):
#                         r_j = r_plane[frame][j, :]
#                         distance = np.linalg.norm(r_i - r_j)
#                         if self._r_grid_min <= distance <= crystal_grid_max:
#                             bx, by, bz = planes[frame][j, :]
#                             angle = np.arccos(
#                                 (ax * bx + ay * by + az * bz) / np.sqrt(
#                                     (ax * ax + ay * ay + az * az) * (bx * bx + by * by + bz * bz)))
#                             data[d, :] = np.array([angle, distance])
#
#             crystal._cvs[self._name] = super()._kde_ovect_rvect(data[:, 0], data[:, 1],
#                                                                 self._r_grid_min, crystal_grid_max,
#                                                                 self._r_bw, crystal_grid_bins,
#                                                                 self._o_grid_min, self._o_grid_max,
#                                                                 self._o_bw, self._o_bins, mirror=mirror)
#
#             # Save output and plot distribution
#             np.savetxt(crystal._path + "pypol_{}_{}_data.dat".format(simulation._name, self._name),
#                        crystal._cvs[self._name],
#                        header="Probability Density Grid.")
#             if plot:
#                 extent = [self._o_grid_min, self._o_grid_max, crystal_grid_max, self._r_grid_min]
#                 plt.imshow(crystal._cvs[self._name], extent=extent, cmap="viridis")
#                 plt.colorbar()
#                 # plt.scatter(data[:, 0], data[:, 1], s=1, facecolor=None, edgecolors='white', alpha=0.025)
#                 plt.xlim(self._o_grid_min, self._o_grid_max)
#                 plt.ylim(self._r_grid_min, crystal_grid_max)
#                 plt.ylabel("RDF / nm")
#                 plt.xlabel("Molecular orientation / rad")
#                 plt.savefig(crystal._path + "pypol_{}_{}_plot.png".format(simulation._name, self._name), dpi=300)
#                 plt.close("all")
#
#     def __str__(self):
#         txt = super(RDFPlanes, self).__str__()
#         if self._r_grid_max:
#             txt += f"""
# Grid Parameters:
# RDF: GRID_MAX={self._r_grid_max} GRID_MIN={self._r_grid_min} GRID_BINS={self._r_bins} BANDWIDTH={self._r_bins}
# Planes: GRID_MAX={self._o_grid_max} GRID_MIN={self._o_grid_min} GRID_BINS={self._o_bins} BANDWIDTH={self._o_bw}
# """
#         else:
#             txt += f"""
# Grid Parameters:
# RDF: GRID_MIN={self._r_grid_min} GRID_SPACING={self._r_grid_space} BANDWIDTH={self._r_bins}
# Planes: GRID_MAX={self._o_grid_max} GRID_MIN={self._o_grid_min} GRID_BINS={self._o_bins} BANDWIDTH={self._o_bw}
# """
#
#         if self._atoms:
#             txt += "\nAtoms:  "
#             for atom in self._atoms:
#                 txt += "{}({})  ".format(atom, self._molecule._atoms[atom]._label)
#         else:
#             txt += "No atoms found in CV {}. Select atoms with the 'set_atoms' module.\n".format(self._name)
#         txt += "\n"
#         return txt
#
#     def _write_output(self, path_output):
#         file_output = open(path_output, "a")
#         file_output.write(self.__str__())
#         file_output.close()
#
#
# # Metadynamics Collective Variables and Walls objects
#
# class Wall(object):
#     """
#     Creates a plumed input file for upper and lower lower WALLS
#     Attributes:\n
#     - name: label for the WALL.
#     - type: Wall.
#     - arg: Inputs for the wall
#     - position: Position of the wall
#     - kappa: Force constant of the wall
#     - offset: The offset for the start of the wall
#     - exp: powers for the wall
#     - eps: the rescaling factor
#     - stride: If possible, the stride used for printing the bias potential in the output file
#     - collective_variable_line: String to be added above the Wall command. This can be used to specify the inputs for
#       the wall (ARG)
#
#     Methods:\n
#     - add_arg(name, kappa=100000, offset=0.0, exp=2, eps=1, at=0.): Add a new input for the wall
#     - reset_arg(name, kappa=100000, offset=0.0, exp=2, eps=1, at=0.): Modify an existing input for the wall
#     """
#
#     def __init__(self, name, position="upper"):
#         """
#         Wall object.
#         :param name: Name given to the variable Wall
#         :param position: "upper" or "lower"
#         """
#
#         position = position.upper()
#         if position not in ("LOWER", "UPPER"):
#             print("Error: Position of the wall not recognized, choose between 'upper' and 'lower'.")
#             exit()
#         self._position = position
#         self._name = name
#         self._type = "Wall"
#         self._arg = list()
#         self._kappa = list()
#         self._offset = list()
#         self._exp = list()
#         self._eps = list()
#         self._at = list()
#         self._stride = 100
#         self._collective_variable_line = ""
#
#     @property
#     def collective_variable_line(self):
#         return self._collective_variable_line
#
#     @collective_variable_line.setter
#     def collective_variable_line(self, values: str):
#         self._collective_variable_line = values
#
#     @property
#     def kappa(self):
#         return self._kappa
#
#     @kappa.setter
#     def kappa(self, values: list):
#         self._kappa = values
#
#     @property
#     def at(self):
#         return self._at
#
#     @at.setter
#     def at(self, values: list):
#         self._at = values
#
#     @property
#     def offset(self):
#         return self._offset
#
#     @offset.setter
#     def offset(self, values: list):
#         self._offset = values
#
#     @property
#     def eps(self):
#         return self._eps
#
#     @eps.setter
#     def eps(self, values: list):
#         self._eps = values
#
#     @property
#     def exp(self):
#         return self._exp
#
#     @exp.setter
#     def exp(self, values: list):
#         self._exp = values
#
#     @property
#     def stride(self):
#         return self._stride
#
#     @stride.setter
#     def stride(self, value: int):
#         self._stride = value
#
#     @property
#     def position(self):
#         return self._position
#
#     @position.setter
#     def position(self, value: str):
#         if value.upper() in ("LOWER", "UPPER"):
#             self._position = value
#         else:
#             print("Error: Position of the wall not recognized, choose between 'upper' and 'lower'.")
#             exit()
#
#     def add_arg(self, name, kappa=100000, offset=0.0, exp=2, eps=1, at=0.):
#         """
#         Add an argument to the Wall object.
#         :param name: Inputs (arg) for the wall
#         :param at: Position of the wall
#         :param kappa: Force constant of the wall
#         :param offset: The offset for the start of the wall
#         :param exp: powers for the wall
#         :param eps: the rescaling factor
#         :return:
#         """
#         self._arg.append(name)
#         self._kappa.append(kappa)
#         self._offset.append(offset)
#         self._exp.append(exp)
#         self._eps.append(eps)
#         self._at.append(at)
#
#     def reset_arg(self, name, kappa=100000, offset=0.0, exp=2, eps=1, at=0.):
#         """
#         Modify an existing argument of the Wall object with the default ones, unless they are specified.
#         :param name: Inputs (arg) for the wall
#         :param at: Position of the wall
#         :param kappa: Force constant of the wall
#         :param offset: The offset for the start of the wall
#         :param exp: powers for the wall
#         :param eps: the rescaling factor
#         :return:
#         """
#
#         if name not in self._arg:
#             print("Error: No ARG with name {}".format(name))
#             exit()
#         i = self._arg.index(name)
#         self._kappa[i] = kappa
#         self._offset[i] = offset
#         self._exp[i] = exp
#         self._eps[i] = eps
#         self._at[i] = at
#
#     def __str__(self):
#         txt = "\nCV: {0._name} ({0._type})\nWall position: {0._position}".format(self)
#         for i in range(len(self._arg)):
#             txt += f"ARG={self._arg[i]} AT={self._at[i]} KAPPA={self._kappa[i]} EXP={self._exp[i]} " \
#                    f"EPS={self._eps[i]} OFFSET={self._offset[i]}\n"
#         return txt
#
#     def _write_output(self, path_output):
#         file_output = open(path_output, "a")
#         file_output.write(self.__str__())
#         file_output.close()
#
#     def _metad(self, print_output=True):
#         if self._collective_variable_line:
#             txt = "\n" + "# Wall\n" + self._collective_variable_line + "\n"
#         else:
#             txt = "\n" + "# Wall\n"
#         args = ",".join(self._arg)
#         at = ",".join([str(a) for a in self._at])
#         kappa = ",".join([str(a) for a in self._kappa])
#         exp = ",".join([str(a) for a in self._exp])
#         eps = ",".join([str(a) for a in self._eps])
#         offset = ",".join([str(a) for a in self._offset])
#         txt += f"""{self._position}_WALLS ...
# ARG={args}
# AT={at}
# KAPPA={kappa}
# EXP={exp}
# EPS={eps}
# OFFSET={offset}
# LABEL={self._name}
# ... {self._position}_WALLS
# """
#
#         if print_output:
#             txt += f"\nPRINT ARG={args},{self._name}.bias FILE={self._name}_COLVAR STRIDE={self._stride}\n"
#         return txt
#
#
# class AvoidScrewedBox(Wall):
#     """
#     Creates a plumed input file forcing the non-diagonal element of the box matrix to stay within a certain range:
#     abs(bx) <= 0.5*ax
#     abs(cx) <= 0.5*ax
#     abs(cy) <= 0.5*by
#     This is done by creating three upper walls with the following attributes:
#     Attributes:\n
#     - name: label for the WALL.
#     - type: "Avoid Screwed Box (Wall)"
#     - arg: [bx,cx,cy]
#     - position: [0.,0.,0.]
#     - kappa: [100000,100000,100000]
#     - offset: [0.1, 0.1, 0.1]
#     - exp: [2,2,2]
#     - eps: [1,1,1]
#     - stride: If possible, the stride used for printing the bias potential in the output file
#     - collective_variable_line: "
#     cell: CELL
#     bx: MATHEVAL ARG=cell.bx,cell.ax FUNC=abs(x)-0.5*y PERIODIC=NO
#     cx: MATHEVAL ARG=cell.cx,cell.ax FUNC=abs(x)-0.5*y PERIODIC=NO
#     cy: MATHEVAL ARG=cell.cy,cell.by FUNC=abs(x)-0.5*y PERIODIC=NO"
#
#     Methods:\n
#     - add_arg(name, kappa=100000, offset=0.0, exp=2, eps=1, at=0.): Add a new input for the wall
#     - reset_arg(name, kappa=100000, offset=0.0, exp=2, eps=1, at=0.): Modify an existing input for the wall
#     """
#
#     def __init__(self, name):
#         """
#
#         :param name:
#         """
#         super(AvoidScrewedBox, self).__init__(name, "UPPER")
#         self._type = "Avoid Screwed Box (Wall)"
#         self._collective_variable_line = """cell: CELL
# bx: MATHEVAL ARG=cell.bx,cell.ax FUNC=abs(x)-0.5*y PERIODIC=NO
# cx: MATHEVAL ARG=cell.cx,cell.ax FUNC=abs(x)-0.5*y PERIODIC=NO
# cy: MATHEVAL ARG=cell.cy,cell.by FUNC=abs(x)-0.5*y PERIODIC=NO"""
#
#         self.add_arg("bx", offset=0.1)
#         self.add_arg("cx", offset=0.1)
#         self.add_arg("cy", offset=0.1)
#
#     def generate_input(self, simulation: MolecularDynamics,
#                        crystals="all",
#                        catt=None):
#
#         """
#         Generate the plumed input files. This is particularly useful for crystals with tilted boxes.
#         If the catt option is used, only crystals with the specified attribute are used.
#         Attributes must be specified in the form of a python dict, menaning catt={"AttributeLabel": "AttributeValue"}.
#         NB: The <simulation>.mdrun_options attribute is modified to include "-plumed plumed_<name>.dat"
#         :param catt: Use crystal attributes to select the crystal list
#         :param simulation: Simulation object
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                          "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                          a specific subset of crystals by listing crystal names.
#         :return:
#         """
#         list_crystals = get_list_crystals(simulation._crystals, crystals, attributes=catt)
#         add_plumed_file = False
#         file_plumed = None
#         if "-plumed" in simulation._mdrun_options:
#             add_plumed_file = input("A plumed file has been found in the mdrun options. \n"
#                                     "Do you want to add it the plumed input (NB: if not, it will be ignored for this "
#                                     "simulation)? [y/n] ")
#             if add_plumed_file.lower() in ("yes", "y", "true"):
#                 add_plumed_file = True
#                 it = iter(simulation._mdrun_options.split())
#                 for i in it:
#                     if i == "-plumed":
#                         file_plumed = next(it)
#             else:
#                 add_plumed_file = False
#         simulation._mdrun_options = " -plumed plumed_{}.dat ".format(self._name)
#         for crystal in list_crystals:
#             txt = self._metad()
#             f = open(crystal._path + "plumed_{}", "w")
#             f.write(txt)
#             if add_plumed_file:
#                 if os.path.exists(crystal._path + file_plumed):
#                     f2 = open(crystal._path + file_plumed, "r")
#                     f.write("".join(f2.readlines()))
#                     f2.close()
#             f.close()
#
#
# class _MetaCV(object):
#     """
#     General Class for Collective Variables.
#     Attributes:\n
#     - name: name of the CV.
#     - cv_type: Type of the CV.
#     - sigma: the bandwidth for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_max: the upper bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     """
#
#     _name = None
#     _sigma = None
#     _grid_bins = None
#     _grid_max = None
#     _grid_min = None
#
#     def __init__(self, name: str,
#                  cv_type: str = "",
#                  sigma: Union[float, list, tuple] = None,
#                  grid_min: Union[float, list, tuple] = None,
#                  grid_max: Union[float, list, tuple] = None,
#                  grid_bins: Union[int, list, tuple] = None,
#                  grid_space: Union[float, list, tuple] = None):
#         """
#         General Class for Collective Variables.
#         :param name: name of the CV.
#         :param cv_type: Type of the CV.
#         :param sigma: the bandwidth for kernel density estimation.
#         :param grid_min: the lower bounds for the grid.
#         :param grid_max: the upper bounds for the grid.
#         :param grid_bins: the number of bins for the grid.
#         :param grid_space: the approximate grid spacing for the grid.
#         """
#         self._name = name
#         self._type = cv_type
#         self._grid_min = grid_min
#         self._grid_max = grid_max
#         self._grid_bins = grid_bins
#         self._grid_space = grid_space
#         self._sigma = sigma
#         self._stride = 100
#
#     @property
#     def stride(self):
#         return self._stride
#
#     @stride.setter
#     def stride(self, value: int):
#         self._stride = value
#
#     @property
#     def sigma(self):
#         return self._sigma
#
#     @sigma.setter
#     def sigma(self, sigma: float):
#         if self._grid_space < sigma * 0.5:
#             self._sigma = sigma
#         else:
#             print("""
# The bin size must be smaller than half the sigma. Choose a sigma greater than {}.
# Alternatively, you can change the bin space or the number of bins.""".format(self._grid_space * 2))
#
#     @property
#     def grid_min(self):
#         return self._grid_min
#
#     @grid_min.setter
#     def grid_min(self, grid_min: float):
#         self._grid_min = grid_min
#         self.grid_space = self._grid_space
#
#     @property
#     def grid_max(self):
#         return self._grid_max
#
#     @grid_max.setter
#     def grid_max(self, grid_max: float):
#         self._grid_max = grid_max
#         self.grid_space = self._grid_space
#
#     @property
#     def grid_bins(self):
#         return self._grid_bins
#
#     @grid_bins.setter
#     def grid_bins(self, grid_bins: int):
#         self._grid_bins = grid_bins
#         if self._grid_max:
#             self._grid_space = (self._grid_max - self._grid_min) / float(self._grid_bins)
#             if self._grid_space > self._sigma * 0.5:
#                 print("The bin size must be smaller than half the bandwidth. Please change the bandwidth accordingly.")
#
#     @property
#     def grid_space(self):
#         return self._grid_space
#
#     @grid_space.setter
#     def grid_space(self, grid_space: float):
#         self._grid_space = grid_space
#         if self._grid_space > self._sigma * 0.5:
#             print("The bin size must be smaller than half the bandwidth. Please change the bandwidth accordingly.")
#         if self._grid_max:
#             self._grid_bins = int((self._grid_max - self._grid_min) / self._grid_space)
#
#     # Read-only properties
#     @property
#     def name(self):
#         return self._name
#
#     def __str__(self):
#         txt = """
# CV: {0._name} ({0._type})
# SIGMA={0._sigma:.3f} GRID_BIN={0._grid_bins} GRID_MAX={0._grid_max:.3f} GRID_MIN={0._grid_min:.3f}""".format(self)
#         return txt
#
#     def _write_output(self, path_output):
#         file_output = open(path_output, "a")
#         file_output.write(self.__str__())
#         file_output.close()
#
#
# class Density(_MetaCV):
#     """
#     Use the density of the crystal as a collective variable
#     Attributes:\n
#     - name: name of the CV.
#     - cv_type: Type of the CV.
#     - sigma: the bandwidth for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_max: the upper bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     - use_walls: Use walls at the upper and lower bounds of the grid to force the system not to escape from it
#     - walls: return a list with the upper and lower walls
#     - uwall: return the upper wall
#     - lwall: return the lower wall
#     """
#
#     def __init__(self, name):
#         """
#         Use the density of the crystal as a collective variable
#         :param name: name of the CV
#         """
#         super().__init__(name, "Density", sigma=10.)
#         self._use_walls = False
#         self._walls = []
#
#     @property
#     def use_walls(self):
#         return self._use_walls
#
#     @use_walls.setter
#     def use_walls(self, value: bool, offset=50.):
#         self._use_walls = value
#         if self._use_walls:
#             if self._grid_max and self._grid_min:
#                 self._walls = [Wall(self._name + "_upper", "UPPER"), Wall(self._name + "_lower", "LOWER")]
#                 self.lwall.add_arg(self._name, at=self._grid_min + offset, kappa=1000)
#                 self.uwall.add_arg(self._name, at=self._grid_max - offset, kappa=1000)
#             else:
#                 print("Error: Define grid_max and grid_min before walls.")
#                 exit()
#
#     @property
#     def walls(self):
#         return self._walls
#
#     @property
#     def uwall(self):
#         if self._walls:
#             return self._walls[0]
#
#     @property
#     def lwall(self):
#         if self._walls:
#             return self._walls[1]
#
#     def _metad(self, value, print_output=True):
#         txt = f"""
# # Density
# {self._name}_vol: VOLUME
# {self._name}: MATHEVAL ARG={self._name}_vol FUNC={value:.3f}/x PERIODIC=NO # FUNC = NMOLS*MW*CONVERSIONFACTOR/VOLUME
# """
#         if self._use_walls:
#             for wall in self._walls:
#                 txt += wall._metad(False)
#
#         if print_output:
#             if self._use_walls:
#                 args = self._walls[0]._name + ".bias," + self._walls[1]._name + ".bias"
#                 txt += f"PRINT ARG={self._name},{args} FILE={self._name}_COLVAR STRIDE={self._stride}"
#             else:
#                 txt += f"PRINT ARG={self._name} FILE={self._name}_COLVAR STRIDE={self._stride}"
#         return txt
#
#
# class PotentialEnergy(_MetaCV):
#     """
#     Use the Potential Energy of the crystal as a collective variable
#     Attributes:\n
#     - name: name of the CV.
#     - cv_type: Type of the CV.
#     - sigma: the bandwidth for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_max: the upper bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     """
#
#     def __init__(self, name):
#         super(PotentialEnergy, self).__init__(name, "Potential Energy", sigma=2.)
#
#     def _metad(self, nmols, imp, remove_bias: list = None, print_output=True):
#         if not remove_bias:
#             txt = f"""
# # Potential Energy Difference
# {self._name}_pot: ENERGY
# {self._name}: MATHEVAL ARG={self._name}_pot VAR=a FUNC=a/{nmols}-{imp} PERIODIC=NO"""
#         else:
#             list_var = list("bcdefghijklmnopqrstuvwxyz")
#             arg = ",".join([i._name + ".bias" for i in remove_bias])
#             var = ",".join([list_var[i] for i in range(len(remove_bias))])
#             func = "-".join([list_var[i] for i in range(len(remove_bias))])
#             txt = f"""
# {self._name}_pot: ENERGY
# {self._name}: MATHEVAL ARG={self._name}_pot,{arg} VAR=a,{var} FUNC=(a-{func})/{nmols}-{imp} PERIODIC=NO\n"""
#
#         if print_output:
#             txt += f"PRINT ARG={self._name} FILE={self._name}_COLVAR STRIDE={self._stride}\n"
#         return txt
#
#
# class _GG(object):
#     """
#     General Class for Groups objects.
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - clustering_type: "classification"
#     """
#
#     def __init__(self, name: str, gtype: str):
#         """
#         Generate Groups From Distribution
#         :param name:
#         :param gtype:
#         """
#
#         # Grouping Properties
#         self._name = name
#         self._type = gtype
#         self._clustering_type = "classification"
#
#     @property
#     def type(self):
#         return self._type
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def clustering_type(self):
#         return self._clustering_type
#
#     def _run(self, simulation, groups, crystals="all", catt=None):
#
#         pd.set_option('display.max_columns', None)
#         pd.set_option('display.max_rows', None)
#         pd.set_option('display.expand_frame_repr', False)
#         pd.set_option('display.max_colwidth', None)
#         pd.set_option('display.max_seq_items', None)
#
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#
#         cvg = {}
#         for i in groups.keys():
#             cvg[i] = 0
#
#         for crystal in list_crystals:
#             crystal._cvs[self._name] = copy.deepcopy(cvg)
#             for group in groups.keys():
#                 if crystal._name in groups[group]:
#                     crystal._cvs[self._name][group] += 1
#                     break
#
#         file_hd = open("{}/Groups_{}_{}.dat".format(simulation._path_output, self._name, simulation._name), "w")
#         file_hd.write("# Group_name             Crystal_IDs\n")
#         for group in groups.keys():
#             file_hd.write("{:<25}: {}\n".format(str(group), groups[group]))
#         file_hd.close()
#
#
# class GGFD(_GG):
#     """
#     Classify structures based on their structural fingerprint.
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - clustering_type: How is it treated by clustering algorithms.
#     - grouping_method: Classification method. It can be based on the distribution similarity or specific patterns.
#     - integration_type: For similarity methods, you can select how the hellinger distance is calculate.
#     - group_threshold: For groups method, the tolerance to define the belonging to a group
#     - kernel: kernel function to use in the histogram generation.
#     - bandwidth: the bandwidths for kernel density estimation.
#     - grid_min: the lower bounds for the grid.
#     - grid_max: the upper bounds for the grid.
#     - grid_bins: the number of bins for the grid.
#     - grid_space: the approximate grid spacing for the grid.
#     - timeinterval: Simulation time interval to generate the distribution.
#
#     Methods:\n
#     - help(): returns available attributes and methods.
#     - set_group_bins(*args, periodic=True, threshold="auto): select boundaries for the groups grouping method.
#     - run(simulation): Creates groups from the crystal distributions in the simulation object.
#     """
#
#     def __init__(self, name: str, cv: Union[Torsions, MolecularOrientation, Density, PotentialEnergy]):
#         """
#         Generate Groups From Distribution
#         :param name:
#         :param cv:
#         """
#         if not cv._type.startswith(("Torsional Angle", "Molecular Orientation", "Density", "Potential Energy")):
#             print("CV not suitable for creating groups.")
#             exit()
#         super(GGFD, self).__init__(name, cv._type)
#         # Grouping Method Properties
#         self._int_type = "discrete"
#         self._grouping_method = "similarity"  # Alternatively, "groups"
#         self._group_threshold = 0.1
#         self._group_bins = {}
#
#         # Original CV Properties (Read-only)
#         self._dist_cv = cv
#         self._kernel = cv._kernel
#         self._bandwidth = cv._bandwidth
#         self._timeinterval = cv._timeinterval
#         if isinstance(cv._grid_bins, int):
#             self._grid_min = [cv._grid_min]
#             self._grid_max = [cv._grid_max]
#             self._grid_bins = [cv._grid_bins]
#             self._D: int = 1
#         else:
#             self._grid_min: Union[list, tuple] = cv._grid_min
#             self._grid_max: Union[list, tuple] = cv._grid_max
#             self._grid_bins: Union[list, tuple] = cv._grid_bins
#             self._D: int = len(cv._grid_bins)
#
#     # Read-only properties
#     @property
#     def cv_kernel(self):
#         return self._kernel
#
#     @property
#     def cv_timeinterval(self):
#         return self._timeinterval
#
#     @property
#     def cv_bandwidth(self):
#         return self._bandwidth
#
#     @property
#     def cv_grid_min(self):
#         return self._grid_min
#
#     @property
#     def cv_grid_max(self):
#         return self._grid_max
#
#     @property
#     def cv_grid_bins(self):
#         return self._grid_bins
#
#     @property
#     def grouping_method(self):
#         return self._grouping_method
#
#     @grouping_method.setter
#     def grouping_method(self, grouping_method: str):
#         if grouping_method.lower() in ("similarity", "groups"):
#             self._grouping_method = grouping_method.lower()
#         else:
#             print("""
# Error: Grouping selection method not recognized. Choose between:
# - 'similarity': Calculate the Hellinger distance between each pair of distributions and group together the similar ones.
# - 'groups':     Group together structures that have non-zero probability density in specified regions of space.""")
#             exit()
#
#     @property
#     def integration_type(self):
#         return self._int_type
#
#     @integration_type.setter
#     def integration_type(self, int_type: str):
#         if int_type.lower() in ("discrete", "simps", "trapz"):
#             self._int_type = int_type.lower()
#         else:
#             print('Error: Hellinger integration type not recognized. Choose between "discrete", "simps" or "trapz"')
#             exit()
#
#     @property
#     def group_threshold(self):
#         return self._group_threshold
#
#     @group_threshold.setter
#     def group_threshold(self, value: float):
#         if 0. < value < 1.:
#             self._group_threshold = value
#         else:
#             print("Group threshold must be between 0 and 1")
#             exit()
#
#     @staticmethod
#     def _non_periodic_dist(step, ibins, bins, grid_bins, grid_min, grid_max, bins_space, threshold):
#         if abs(grid_min - bins[0]) > threshold:
#             bins = [grid_min] + bins
#         if abs(grid_max - bins[-1]) > threshold:
#             bins = bins[:-1]
#         ibins[(step, 0)] = [j for j in range(grid_bins) if j * bins_space + grid_min < bins[1]]
#         ibins[(step, len(bins) - 1)] = [j for j in range(grid_bins) if bins[-1] <= j * bins_space + grid_min]
#         return ibins, bins
#
#     @staticmethod
#     def _periodic_dist(step, ibins, bins, grid_bins, grid_min, bins_space):
#         bins = [grid_min] + bins
#         ibins[(step, 0)] = [j for j in range(grid_bins) if j * bins_space + grid_min < bins[1]] + \
#                            [j for j in range(grid_bins) if bins[-1] <= j * bins_space + grid_min]
#         return ibins, bins
#
#     def __str__(self):
#         txt = """
# CV: {0._name} ({0._type})
# Clustering Type: {0._clustering_type}
# Grouping Method: {0._grouping_method}
# Threshold: {0._group_threshold}\n""".format(self)
#         if self._grouping_method == "groups" and self._group_bins:
#             for k, item in self._group_bins.items():
#                 txt += "{}: {}\n".format(k, item)
#         return txt
#
#     def _write_output(self, path_output):
#         file_output = open(path_output, "a")
#         file_output.write(self.__str__())
#         file_output.close()
#
#     @staticmethod
#     def help():
#         return """
# Classify structures based on their structural fingerprint .
# Attributes:
# - name: name of the CV.
# - type: Type of the CV.
# - clustering_type: How is it treated by clustering algorithms.
# - grouping_method: Classification method. It can be based on the distribution similarity or specific patterns:
#             - 'similarity': Calculate the Hellinger distance between each pair of distributions and group
#                             together the similar ones.
#             - 'groups':     Group together structures that have non-zero probability density in specified regions
#                             of space.
# - integration_type: For similarity methods, you can select how the hellinger distance is calculate.
#             Choose between "discrete", "simps" or "trapz"
# - group_threshold: For groups method, if the probability density in a specific region of space is lower than this
#             value, then it is assumed that no molecules are that area.
# - kernel: kernel function to use in the histogram generation.
# - bandwidth: the bandwidths for kernel density estimation.
# - grid_min: the lower bounds for the grid.
# - grid_max: the upper bounds for the grid.
# - grid_bins: the number of bins for the grid.
# - grid_space: the approximate grid spacing for the grid.
# - timeinterval: Simulation time interval to generate the distribution.
#
# Methods:
# - help(): returns available attributes and methods.
# - set_group_bins(*args, periodic=True, threshold="auto): select boundaries for the groups grouping method. args must be
#                 iterable objects. If periodic = False, an additional boundary is put at the grid max and min.
# - run(simulation): Creates groups from the crystal distributions in the simulation object.
#
# Examples:
# - Group structures by similarity:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# tor = gaff.get_cv("tor")                                      # Retrieve the CV Object
# conf = gaff.ggfd("conf", tor)                                 # Create the GGFD object
# conf.grouping_method = "similarity"                           # Use the similarity grouping method
# conf.integration_type = "simps"                               # Use the simps method to calculate the hellonger distance
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# conf.run(tor)                                                 # Generates groups
# project.save()
#
# - Group structures by similarity:
# from PyPol import pypol as pp
# project = pp.load_project(r'/home/Work/Project/')             # Load project from the specified folder
# gaff = project.get_method('GAFF')                             # Retrieve an existing method
# tor = gaff.get_cv("tor")                                      # Retrieve the CV Object (2D torsional angle)
# conf = gaff.ggfd("conf", tor)                                 # Create the GGFD object
# conf.grouping_method = "groups"                               # Use the "groups" grouping method
# conf.group_threshold = 0.1                                    # Cutoff for determining which areas are occupied
# conf.set_group_bins((-2., 0, 2.),(-1., 2.), periodic=True)    # Define the group boundaries in the (2D) CV space
# npt = gaff.get_simulation("npt")                              # Retrieve a completed simulation
# conf.run(tor)                                                 # Generates groups
# project.save()
# """
#
#     def set_group_bins(self, *args: Union[list, tuple], periodic: bool = True):  # , threshold="auto"
#         # TODO Change args to dict with key == names of the variables.
#         #  As it is right now you have to remember the order in which ND dimensional distribution are added together.
#         """
#         Select boundaries for the groups grouping method. args must be iterable objects.
#         If periodic = False, an additional boundary is put at the grid max and min.
#         :param args: A list or a tuple of the dividing boundaries in a distribution. The number of boundaries must be
#                equal to the dimension of the distribution.
#         :param periodic: If True, periodic conditions are applied to the grouping algorithm. Mixing periodic and
#                non-periodic boundaries can be done by setting periodic=True and adding a 0. to the boundary list in
#                which it is not true
#         :return:
#         """
#         args = list(args)
#         if len(args) != self._D:
#             print("Error: incorrect number of args, {} instead of {}.".format(len(args), self._D))
#             exit()
#
#         self._group_bins = {}
#         for i in range(self._D):
#             bins = list(args[i])
#             bins_space = (self._grid_max[i] - self._grid_min[i]) / self._grid_bins[i]
#
#             # if threshold == "auto":
#             threshold = 0.5 * (self._grid_max[i] - self._grid_min[i]) / self._grid_bins[i]
#
#             if not periodic:
#                 self._group_bins, bins = self._non_periodic_dist(i, self._group_bins, bins, self._grid_bins[i],
#                                                                  self._grid_min[i], self._grid_max[i], bins_space,
#                                                                  threshold)
#
#             else:
#                 if abs(self._grid_min[i] - bins[0]) < threshold or abs(self._grid_max[i] - bins[-1]) < threshold:
#                     self._group_bins, bins = self._non_periodic_dist(i, self._group_bins, bins, self._grid_bins[i],
#                                                                      self._grid_min[i], self._grid_max[i], bins_space,
#                                                                      threshold)
#                 else:
#                     self._group_bins, bins = self._periodic_dist(i, self._group_bins, bins, self._grid_bins[i],
#                                                                  self._grid_min[i], bins_space)
#
#             for b in range(1, len(bins) - 1):
#                 self._group_bins[(i, b)] = [j for j in range(self._grid_bins[i])
#                                             if bins[b] < j * bins_space + self._grid_min[i] <= bins[b + 1]]
#
#     def run(self,
#             simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#             crystals="all", catt=None):
#         """
#         Creates groups from the crystal distributions in the simulation object.
#         :param simulation: Simulation Object (EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics)
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                a specific subset of crystals by listing crystal names.
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#
#         pd.set_option('display.max_columns', None)
#         pd.set_option('display.max_rows', None)
#         pd.set_option('display.expand_frame_repr', False)
#         pd.set_option('display.max_colwidth', None)
#         pd.set_option('display.max_seq_items', None)
#
#         groups = {}
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#
#         if self._grouping_method == "groups":
#             combinations: list = []
#             for i in range(self._D):
#                 combinations.append([c for c in self._group_bins.keys() if c[0] == i])
#
#             # noinspection PyTypeChecker
#             dataset = np.full((len(list_crystals), len((list(its.product(*combinations)))) + 1), np.nan)
#             index = []
#             for cidx in range(len(list_crystals)):
#                 crystal = list_crystals[cidx]
#
#                 index.append(crystal._name)
#                 dist = crystal._cvs[self._dist_cv._name] / np.sum(crystal._cvs[self._dist_cv._name])
#                 c = 0
#                 for i in its.product(*combinations):
#                     dataset[cidx, c] = np.sum(dist[np.ix_(self._group_bins[i[0]], self._group_bins[i[1]])])
#                     c += 1
#
#             dataset = pd.DataFrame(np.where(dataset > self._group_threshold, 1, 0), index=index,
#                                    columns=[(i[0][1], i[1][1]) for i in its.product(*combinations)] + ["Others"])
#
#             groups = dataset.groupby(dataset.columns.to_list()).groups
#             groups = {k: groups[k].to_list() for k in sorted(groups.keys(), key=lambda x: np.sum(x))}
#
#         elif self._grouping_method == "similarity":
#             from scipy.sparse import csr_matrix
#             from scipy.sparse.csgraph import breadth_first_order
#             index = []
#             for crystal in list_crystals:
#                 index.append(crystal._name)
#
#             dmat = pd.DataFrame(np.zeros((len(index), len(index))), columns=index, index=index)
#             bar = progressbar.ProgressBar(maxval=int(len(crystals) * (len(crystals) - 1) / 2)).start()
#             nbar = 1
#
#             for i in range(len(list_crystals) - 1):
#                 from copy import deepcopy
#                 di = deepcopy(list_crystals[i]._cvs[self._dist_cv._name])
#                 ci = list_crystals[i]._name
#                 for j in range(i + 1, len(crystals)):
#                     dj = deepcopy(list_crystals[j]._cvs[self._dist_cv._name])
#                     cj = list_crystals[j]._name
#                     bar.update(nbar)
#                     nbar += 1
#                     if self._dist_cv._type == "Radial Distribution Function":  # ?
#                         if len(di) > len(dj):
#                             hd = hellinger(di.copy()[:len(dj)], dj.copy(), self._int_type)
#                         else:
#                             hd = hellinger(di.copy(), dj.copy()[:len(di)], self._int_type)
#                     else:
#                         hd = hellinger(di.copy(), dj.copy(), self._int_type)
#                     dmat.at[ci, cj] = dmat.at[cj, ci] = hd
#             bar.finish()
#
#             dmat = pd.DataFrame(np.where(dmat.values < self._group_threshold, 1., 0.), columns=index, index=index)
#
#             graph = csr_matrix(dmat)
#             removed = []
#             for c in range(len(dmat.index)):
#                 if dmat.index.to_list()[c] in removed:
#                     continue
#                 bfs = breadth_first_order(graph, c, False, False)
#                 group_index = [index[i] for i in range(len(index)) if i in bfs]
#                 removed = removed + group_index
#                 groups[group_index[0]] = group_index
#
#         self._run(simulation, groups, crystals)
#
#
# class GGFA(_GG):
#     """
#     Classify structures based on their attributes.
#     Attributes:\n
#     - name: name of the CV.
#     - type: Type of the CV.
#     - clustering_type: "classification"
#     - attribute: Attribute label to be used for classification
#
#     Methods:\n
#     - help(): returns available attributes and methods. (TODO)
#     - run(simulation): Creates groups looking at the crystal attributes in the simulation object
#     """
#
#     def __init__(self, name: str, attribute: str):
#         """
#         Generate Groups From Attributes
#         :param name: Group Label.
#         :param attribute: Attribute label to be used for classification.
#         """
#
#         # Grouping Properties
#         super().__init__(name, "Attribute")
#
#         self._attribute = attribute
#
#     @property
#     def attribute(self):
#         return self._attribute
#
#     def run(self,
#             simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#             crystals="all", catt=None):
#         """
#         Creates groups from the crystal attributes in the simulation object.
#         :param simulation: Simulation Object (EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics)
#         :param crystals: It can be either "all", use all non-melted Crystal objects from the previous simulation or
#                "centers", use only cluster centers from the previous simulation. Alternatively, you can select
#                a specific subset of crystals by listing crystal names.
#         :param catt: Use crystal attributes to select the crystal list
#         :return:
#         """
#
#         pd.set_option('display.max_columns', None)
#         pd.set_option('display.max_rows', None)
#         pd.set_option('display.expand_frame_repr', False)
#         pd.set_option('display.max_colwidth', None)
#         pd.set_option('display.max_seq_items', None)
#
#         groups = {}
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#
#         if not all(self._attribute in crystal._attributes for crystal in list_crystals):
#             print(f"Error: some of the Crystals do not have attribute '{self._attribute}'")
#             exit()
#
#         for crystal in list_crystals:
#             gatt = crystal._attributes[self._attribute]
#             if gatt in groups:
#                 groups[gatt].append(crystal._name)
#             else:
#                 groups[gatt] = [crystal._name]
#
#         self._run(simulation, groups, crystals)
#
#     def __str__(self):
#         return """
# CV: {0._name} ({0._type})
# Clustering Type: {0._clustering_type}
# """.format(self)
#
#     def _write_output(self, path_output):
#         file_output = open(path_output, "a")
#         file_output.write(self.__str__())
#         file_output.close()
#
#
# #
# # Utilities
# #
#
# def generate_atom_list(atoms, molecule, crystal, keyword="ATOMS", lines=None, index_lines=True, attributes=None):
#     """
#     Generates the atom list used in the plumed input.
#
#     :param atoms: Atoms used by the CV
#     :param molecule: Molecule from which the atoms' index are taken
#     :param crystal: Crystal object from which the molecules are taken
#     :param keyword: String put before the atoms' index
#     :param lines: string to which new lines are appended
#     :param index_lines: starting index for the variable "keyword"
#     :param attributes: Molecular attributes used to select the molecules
#     :return:
#     """
#     if attributes is None:
#         attributes = {}
#     if lines is None:
#         lines = []
#
#     idx_mol = len(lines) + 1
#
#     if attributes:
#         mols = []
#         for mol in crystal._load_coordinates():
#             if attributes.items() <= mol._attributes.items():
#                 mols.append(mol)
#     else:
#         mols = crystal._load_coordinates()
#
#     for mol in mols:
#         if molecule._residue == mol._residue:
#             if index_lines:
#                 line = "{}{}=".format(keyword, idx_mol)
#             else:
#                 line = "{}=".format(keyword)
#             for atom in atoms:
#                 atom_idx = atom + mol._index * mol._natoms + 1
#                 line += str(atom_idx) + ","
#             line = line[:-1] + "\n"
#             lines.append(line)
#             idx_mol += 1
#     crystal._molecules = list()
#     return lines
#
#
# #
# # Clustering analysis
# #
#
#
# class Clustering(object):
#
#     def __init__(self, name, cvs):
#         self._name = name
#         self._cvp = cvs
#
#         self._int_type = "discrete"
#         self._algorithm = "fsfdp"  # Only method available
#         self._kernel = "gaussian"
#         self._centers = "energy"
#         self._d_c = []
#         self._d_c_fraction = 0.01
#         self._sigma_cutoff = False
#
#         self._distance_matrix = False
#         self._cluster_data = {}
#         self._clusters = {}
#
#     # Read-only Properties
#     @property
#     def d_c(self):
#         if isinstance(self._d_c, float):
#             return self._d_c
#         else:
#             print("d_c has not been calculated yet. Generate the distance matrix to visualize it.")
#
#     @property
#     def distance_matrix(self):
#         return self._distance_matrix
#
#     @property
#     def clustering_algorithm(self):
#         return self._algorithm
#
#     @property
#     def clusters(self):
#         return self._clusters
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def cvs(self):
#         txt = "Collective Variables:\n"
#         for cv in self._cvp:
#             txt += cv._name + "\n"
#         return txt
#
#     # Properties
#
#     @property
#     def sigma_cutoff(self):
#         return self._sigma_cutoff
#
#     @sigma_cutoff.setter
#     def sigma_cutoff(self, value):
#         if 0. < value < 1.:
#             self._sigma_cutoff = value
#         else:
#             print(r"The cutoff must be between 0 and 1.")
#
#     @property
#     def d_c_neighbors_fraction(self):
#         return self._d_c_fraction
#
#     @d_c_neighbors_fraction.setter
#     def d_c_neighbors_fraction(self, value: float):
#         if 0. < value < 1.:
#             self._d_c_fraction = value
#             if value > 0.05:
#                 print("The average number of neighbors should be between 1% and 5% of the total number of points."
#                       "Fractions higher than 0.05 could cause problems in the analysis.")
#         else:
#             print(r"The neighbors fraction must be between 0 and 1. The average number of neighbors should be between "
#                   r"1% and 5% of the total number of points.")
#
#     @property
#     def hellinger_integration_type(self):
#         return self._int_type
#
#     @hellinger_integration_type.setter
#     def hellinger_integration_type(self, int_type):
#         if int_type.lower() in ("discrete", "simps", "trapz"):
#             self._int_type = int_type.lower()
#         else:
#             print('Error: Hellinger integration type not recognized. Choose between "discrete", "simps" or "trapz"')
#             exit()
#
#     @property
#     def center_selection(self):
#         return self._centers
#
#     @center_selection.setter
#     def center_selection(self, center_selection):
#         if center_selection.lower() in ("energy", "cluster_center"):
#             self._centers = center_selection.lower()
#         else:
#             print("Error: Center selection method not recognized. Choose between:\n"
#                   "'energy'        : select structure with the lower potential energy in the group as cluster center.\n"
#                   "'cluster_center': select the cluster center resulting from the clustering algorithm.")
#             exit()
#
#     @property
#     def kernel(self):
#         return self._kernel
#
#     @kernel.setter
#     def kernel(self, kernel):
#         if kernel.lower() in ("gaussian", "cutoff"):
#             self._kernel = kernel.lower()
#         else:
#             print("Error: Kernel function not recognized. Choose between 'gaussian' and 'cutoff'")
#             exit()
#
#     @staticmethod
#     def _sort_crystal(crystal, combinations, threshold=0.8):
#         for i in combinations.index[:-1]:
#             for j in combinations.columns[:-2]:
#                 if crystal._cvs[j][combinations.loc[i, j]] > threshold and j == combinations.columns[-3]:
#                     combinations.loc[i, "Structures"].append(crystal)
#                     combinations.loc[i, "Number of structures"] += 1
#                     return combinations
#                 elif crystal._cvs[j][combinations.loc[i, j]] < threshold:
#                     break
#         combinations.loc["Others", "Structures"].append(crystal)
#         combinations.loc["Others", "Number of structures"] += 1
#         return combinations
#
#     def run(self,
#             simulation: Union[EnergyMinimization, CellRelaxation, MolecularDynamics, Metadynamics],
#             crystals="all",
#             group_threshold: float = 0.8,
#             gen_sim_mat: bool = True,
#             catt=None,
#             _cv_name=""):
#         self._clusters = {}
#         self._cluster_data = {}
#         list_crystals = get_list_crystals(simulation._crystals, crystals, catt)
#         pd.set_option('display.max_columns', None)
#         pd.set_option('display.max_rows', None)
#         pd.set_option('display.expand_frame_repr', False)
#         pd.set_option('display.max_colwidth', None)
#         pd.set_option('display.max_seq_items', None)
#
#         if not simulation._completed:
#             print("Simulation {} is not completed yet. Run simulation.get_results() to check termination and import "
#                   "results.".format(simulation._name))
#
#         path_output = simulation._path_output + str(self._name) + "_data/"
#         if not os.path.exists(path_output):
#             os.mkdir(path_output)
#
#         if gen_sim_mat:
#             self._d_c = []
#             group_options = []
#             group_names = []
#             for cv in self._cvp:
#                 if cv.clustering_type == "classification":
#                     for crystal in list_crystals:
#                         group_options.append(list(crystal._cvs[cv._name].keys()))
#                         group_names.append(cv._name)
#                         break
#             if group_options:
#                 if len(group_names) == 1:
#                     combinations = group_options[0] + [None]
#                     index = [str(i) for i in range(len(combinations) - 1)] + ["Others"]
#                     combinations = pd.concat((pd.Series(combinations, name=group_names[0], index=index),
#                                               pd.Series([0 for _ in range(len(combinations))],
#                                                         name="Number of structures", dtype=int, index=index),
#                                               pd.Series([[] for _ in range(len(combinations))], name="Structures",
#                                                         index=index)), axis=1)
#                 else:
#
#                     combinations = list(its.product(*group_options)) + \
#                                    [tuple([None for _ in range(len(group_options[0]))])]
#                     index = [str(i) for i in range(len(combinations) - 1)] + ["Others"]
#                     combinations = pd.concat((pd.DataFrame(combinations, columns=group_names, index=index),
#                                               pd.Series([0 for _ in range(len(combinations))],
#                                                         name="Number of structures", dtype=int, index=index),
#                                               pd.Series([[] for _ in range(len(combinations))], name="Structures",
#                                                         index=index)), axis=1)
#                 combinations.index.name = "Combinations"
#                 bar = progressbar.ProgressBar(maxval=len(list_crystals)).start()
#                 nbar = 1
#                 for crystal in list_crystals:
#                     combinations = self._sort_crystal(crystal, combinations, group_threshold)
#                     bar.update(nbar)
#                     nbar += 1
#                 bar.finish()
#
#             else:
#                 combinations = pd.DataFrame([[0, []]], columns=["Number of structures", "Structures"],
#                                             dtype=None, index=["all"])
#                 combinations.index.name = "Combinations"
#                 for crystal in list_crystals:
#                     combinations.loc["all", "Structures"].append(crystal)
#                     combinations.loc["all", "Number of structures"] += 1
#
#             slist = [np.full((combinations.loc[i, "Number of structures"],
#                               combinations.loc[i, "Number of structures"]), 0.0) for i in combinations.index]
#             combinations = pd.concat((combinations,
#                                       pd.Series(slist, name="Distance Matrix", index=combinations.index)), axis=1)
#
#             # Generate Distance Matrix of each set of distributions
#             distributions = [cv for cv in self._cvp if cv.clustering_type != "classification"]
#             n_factors = {}
#             for cv in distributions:
#                 combinations[cv._name] = pd.Series(copy.deepcopy(combinations["Distance Matrix"].to_dict()),
#                                                    index=combinations.index)
#                 n_factors[cv._name] = 0.
#
#                 for index in combinations.index:
#                     if combinations.at[index, "Number of structures"] > 1:
#                         crystals = combinations.at[index, "Structures"]
#
#                         print("\nCV: {} Group: {}".format(cv._name, index))
#                         bar = progressbar.ProgressBar(maxval=int(len(crystals) * (len(crystals) - 1) / 2)).start()
#                         nbar = 1
#
#                         for i in range(len(crystals) - 1):
#                             di = crystals[i]._cvs[cv._name]
#                             for j in range(i + 1, len(crystals)):
#                                 dj = crystals[j]._cvs[cv._name]
#                                 bar.update(nbar)
#                                 nbar += 1
#                                 if di.shape != dj.shape:
#                                     di = di.copy()[tuple(map(slice, dj.shape))]
#                                     dj = dj.copy()[tuple(map(slice, di.shape))]
#
#                                 # if cv._type == "Radial Distribution Function":
#                                 #     if len(di) > len(dj):
#                                 #         hd = hellinger(di.copy()[:len(dj)], dj.copy(), self._int_type)
#                                 #     else:
#                                 #         hd = hellinger(di.copy(), dj.copy()[:len(di)], self._int_type)
#                                 #
#                                 # else:
#                                 #     hd = hellinger(di.copy(), dj.copy(), self._int_type)
#                                 hd = hellinger(di.copy(), dj.copy(), self._int_type)
#                                 combinations.loc[index, cv._name][i, j] = combinations.loc[index, cv._name][j, i] = hd
#
#                                 if hd > n_factors[cv._name]:
#                                     n_factors[cv._name] = hd
#                         bar.finish()
#
#             # Normalize distances
#             print("Normalization...", end="")
#             normalization = []
#             for cv in distributions:
#                 normalization.append(1. / n_factors[cv._name])
#                 for index in combinations.index:
#                     if combinations.at[index, "Number of structures"] > 1:
#                         combinations.at[index, cv._name] /= n_factors[cv._name]
#             print("done")
#
#             # Generate Distance Matrix
#             print("Generating Distance Matrix...", end="")
#             normalization = np.linalg.norm(np.array(normalization))
#             for index in combinations.index:
#                 if combinations.at[index, "Number of structures"] > 1:
#                     for i in range(combinations.at[index, "Number of structures"] - 1):
#                         for j in range(i + 1, combinations.at[index, "Number of structures"]):
#                             dist_ij = np.linalg.norm([k[i, j] for k in
#                                                       combinations.loc[index, [cv._name for cv in distributions]]])
#                             combinations.at[index, "Distance Matrix"][i, j] = \
#                                 combinations.at[index, "Distance Matrix"][j, i] = dist_ij / normalization
#                             self._d_c.append(dist_ij)
#
#             for index in combinations.index:
#                 if combinations.at[index, "Number of structures"] > 1:
#                     idx = [i._name for i in combinations.at[index, "Structures"]]
#                     for mat in combinations.loc[index, "Distance Matrix":].index:
#                         combinations.at[index, mat] = pd.DataFrame(combinations.at[index, mat], index=idx, columns=idx)
#                         with open(path_output + mat.replace(" ", "") + "_" + index + ".dat", 'w') as fo:
#                             fo.write(combinations.loc[index, mat].__str__())
#
#             for i in combinations.loc[:, "Distance Matrix":].columns:
#                 total = pd.concat([m for m in combinations.loc[:, i] if not isinstance(m, np.ndarray)])
#                 total.to_csv(simulation._path_output + str(self._name) + "_" + i.replace(" ", "") + ".dat")
#                 # with open(, 'w') as fo:
#                 #     fo.write(total.__str__())
#                 plt.imshow(total, interpolation="nearest", cmap="viridis")
#                 plt.colorbar()
#                 plt.tight_layout()
#                 plt.savefig(simulation._path_output + str(self._name) + "_" + i.replace(" ", "") + ".png", dpi=300)
#                 plt.close('all')
#
#             self._distance_matrix = combinations
#
#             list_crys = [[i._name for i in row["Structures"]] for index, row in self._distance_matrix.iterrows()]
#             file_output = pd.concat((self._distance_matrix.loc[:, :"Number of structures"],
#                                      pd.Series(list_crys, name="IDs", index=self._distance_matrix.index)), axis=1)
#
#             with open(simulation._path_output + str(self._name) + "_Groups.dat", 'w') as fo:
#                 fo.write("Normalization Factors:\n")
#                 for n in n_factors.keys():
#                     fo.write("{:15}: {:<1.3f}\n".format(n, n_factors[n]))
#                 fo.write(file_output.__str__())
#             print("done")
#             self._d_c = np.sort(np.array(self._d_c))[int(float(len(self._d_c)) * self._d_c_fraction)]
#
#         # Remove structures that are not cluster centers
#         print("Clustering...", end="")
#         changes_string = ""
#         with open(simulation._path_output + str(self._name) + "_FSFDP.dat", 'w') as fo:
#             fo.write("# FSFDP parameters for every group:\n")
#
#         for index in self._distance_matrix.index:
#             if int(self._distance_matrix.at[index, "Number of structures"]) == 0:
#                 continue
#             elif int(self._distance_matrix.at[index, "Number of structures"]) == 1:
#                 nc = self._distance_matrix.at[index, "Structures"][0]._name
#                 columns = ["rho", "sigma", "NN", "cluster", "distance"]
#                 self._cluster_data[index] = pd.DataFrame([[0, 0, pd.NA, nc, 0]], index=[nc], columns=columns)
#                 self._clusters[index] = {nc: [nc]}
#             elif int(self._distance_matrix.at[index, "Number of structures"]) == 2:
#                 nc1 = self._distance_matrix.at[index, "Structures"][0]._name
#                 nc2 = self._distance_matrix.at[index, "Structures"][1]._name
#                 columns = ["rho", "sigma", "NN", "cluster", "distance"]
#                 d_12 = self._distance_matrix.at[index, "Distance Matrix"].values[0, 1]
#                 if d_12 > self._d_c:
#                     self._cluster_data[index] = pd.DataFrame([[0, 0, nc2, nc1, 0], [0, 0, nc1, nc2, 0]],
#                                                              index=[nc1, nc2], columns=columns)
#                     self._clusters[index] = {nc1: [nc1], nc2: [nc2]}
#                 else:
#                     self._cluster_data[index] = pd.DataFrame([[0, 0, nc2, nc1, 0], [0, 0, nc1, nc1, d_12]],
#                                                              index=[nc1, nc2], columns=columns)
#                     self._clusters[index] = {nc1: [nc1, nc2]}
#             elif int(self._distance_matrix.at[index, "Number of structures"]) > 2:
#                 if self._algorithm == "fsfdp":
#                     self._cluster_data[index], sc = FSFDP(self._distance_matrix.at[index, "Distance Matrix"],
#                                                           kernel=self._kernel,
#                                                           d_c=self._d_c,
#                                                           d_c_neighbors_fraction=self._d_c_fraction,
#                                                           sigma_cutoff=self._sigma_cutoff)
#                     _save_decision_graph(self._cluster_data[index].loc[:, "rho"].values,
#                                          self._cluster_data[index].loc[:, "sigma"].values,
#                                          sigma_cutoff=sc,
#                                          path=path_output + "Decision_graph_" + str(index) + ".png")
#
#                     with open(path_output + "FSFDP_" + str(index) + ".dat", 'w') as fo:
#                         fo.write(self._cluster_data[index].__str__())
#
#                     with open(simulation._path_output + str(self._name) + "_FSFDP.dat", 'a') as fo:
#                         fo.write("\n# Group {}\n".format(str(index)))
#                         fo.write(self._cluster_data[index].__str__())
#
#                 self._clusters[index] = {
#                     k: self._cluster_data[index].index[self._cluster_data[index]["cluster"] == k].tolist()
#                     for k in list(self._cluster_data[index]["cluster"].unique())}
#
#             if self._centers.lower() == "energy":
#                 new_clusters = copy.deepcopy(self._clusters[index])
#                 energies = {k._name: k._energy for k in self._distance_matrix.at[index, "Structures"]}
#                 for center in self._clusters[index].keys():
#                     changes = [center, None]
#                     emin = energies[center]
#                     for crystal in self._clusters[index][center]:
#                         if energies[crystal] < emin:
#                             changes[1] = crystal
#                             emin = energies[crystal]
#                     if changes[1]:
#                         new_clusters[changes[1]] = new_clusters.pop(changes[0])
#                         changes_string += "{:>25} ---> {:25}\n".format(changes[0], changes[1])
#                 self._clusters[index] = new_clusters
#
#             for crystal in self._distance_matrix.at[index, "Structures"]:
#                 for cc in self._clusters[index].keys():
#                     if crystal._name in self._clusters[index][cc]:
#                         crystal._state = cc
#                         break
#         cluster_groups = [g for g in self._clusters.keys() for _ in self._clusters[g].keys()]
#         self._clusters = {k: v for g in self._clusters.keys() for k, v in self._clusters[g].items()}
#         self._clusters = pd.concat((
#             pd.Series(data=[len(self._clusters[x]) for x in self._clusters.keys()], index=self._clusters.keys(),
#                       name="Number of Structures"),
#             pd.Series(data=cluster_groups, index=self._clusters.keys(), name="Group"),
#             pd.Series(data=[", ".join(str(y) for y in self._clusters[x]) for x in self._clusters.keys()],
#                       index=self._clusters.keys(), name="Structures")),
#             axis=1).sort_values(by="Number of Structures", ascending=False)
#
#         with open(simulation._path_output + str(self._name) + "_Clusters.dat", 'w') as fo:
#             if changes_string:
#                 fo.write("Cluster centers changed according to potential energy:\n")
#                 fo.write(changes_string)
#             fo.write(self._clusters.__str__())
#
#         with open(simulation._path_output + str(self._name) + "_DFC.dat", 'w') as fo:
#             if changes_string:
#                 fo.write("Cluster centers changed according to potential energy:\n")
#                 fo.write(changes_string)
#             total = pd.concat([m for m in self._distance_matrix.loc[:, "Distance Matrix"]
#                                if not isinstance(m, np.ndarray)])
#             index = []
#             centers = []
#             distances = []
#             for crystal in get_list_crystals(simulation._crystals, crystals=total.index.to_list()):
#                 index.append(crystal._name)
#                 centers.append(crystal._state)
#                 distances.append(total.at[crystal._name, crystal._state])
#             dfc = pd.DataFrame({"Center": centers, "Distance": distances}, index=index).sort_values(by="Distance")
#             fo.write(dfc.__str__())
#         print("done")
#
#
# def hellinger(y1: Union[np.array, list],
#               y2: Union[np.array, list],
#               int_type: str = "discrete"):
#     """
#
#     :param y1:
#     :param y2:
#     :param int_type:
#     :return:
#     """
#     y1 = copy.deepcopy(y1)
#     y2 = copy.deepcopy(y2)
#     if int_type == "discrete":
#         # Normalise Distributions
#         y1 /= np.sum(y1)
#         y2 /= np.sum(y2)
#
#         BC = np.sum(np.sqrt(np.multiply(y1, y2)))
#         HD = round(np.sqrt(1 - BC), 5)
#         return HD
#
#     elif int_type == "simps":
#         from scipy.integrate import simps
#         # Normalise Distributions
#         N1, N2 = (y1, y2)
#         for x in y1.shape:
#             N1 = simps(N1, np.linspace(0, x - 1, x))
#             N2 = simps(N2, np.linspace(0, x - 1, x))
#         y1 /= N1
#         y2 /= N2
#
#         BC = np.sqrt(np.multiply(y1, y2))
#         for x in y1.shape:
#             BC = simps(BC, np.linspace(0, x - 1, x))
#         HD = round(np.sqrt(1 - BC), 5)
#         return HD
#
#     elif int_type == "trapz":
#         from scipy.integrate import trapz
#         # Normalise Distributions
#         N1, N2 = (y1, y2)
#         for x in y1.shape:
#             N1 = trapz(N1, np.linspace(0, x - 1, x))
#             N2 = trapz(N2, np.linspace(0, x - 1, x))
#         y1 /= N1
#         y2 /= N2
#
#         BC = np.sqrt(np.multiply(y1, y2))
#         for x in y1.shape:
#             BC = trapz(BC, np.linspace(0, x - 1, x))
#         HD = round(np.sqrt(1 - BC), 5)
#         return HD
#
#     else:
#         print("Error: choose integration type among 'simps', 'trapz' or 'discrete'.")
#         exit()
#
#
# def _decision_graph(x, y):
#     class PointPicker(object):
#         def __init__(self, ppax, ppscat, clicklim=0.05):
#             self.fig = ppax.figure
#             self.ax = ppax
#             self.scat = ppscat
#             self.clicklim = clicklim
#             self.sigma_cutoff = 0.1
#             self.horizontal_line = ppax.axhline(y=.1, color='red', alpha=0.5)
#             self.text = ppax.text(0, 0.5, "")
#             self.fig.canvas.mpl_connect('button_press_event', self.onclick)
#
#         def onclick(self, event):
#             if event.inaxes == self.ax:
#                 self.sigma_cutoff = event.ydata
#                 xlim0, xlim1 = ax.get_xlim()
#                 self.horizontal_line.set_ydata(self.sigma_cutoff)
#                 self.text.set_text(str(round(self.sigma_cutoff, 5)))
#                 self.text.set_position((xlim0, self.sigma_cutoff))
#                 colors = []
#                 for i in self.scat.get_offsets():
#                     if i[1] >= self.sigma_cutoff:
#                         colors.append("C0")
#                     else:
#                         colors.append("C1")
#                 self.scat.set_color(colors)
#                 self.fig.canvas.draw()
#
#     fig = plt.figure()
#
#     ax = fig.add_subplot(111)
#     scat = ax.scatter(x, y, color="C0", alpha=0.25)
#
#     plt.title(r"Select $\sigma$-cutoff and quit to continue", fontsize=20)
#     plt.xlabel(r"$\rho$", fontsize=20)
#     plt.ylabel(r"$\delta$", fontsize=20)
#     p = PointPicker(ax, scat)
#     plt.show()
#     return p.sigma_cutoff
#
#
# def _save_decision_graph(rho, sigma, sigma_cutoff, path):
#     for i in range(len(rho)):
#         if sigma[i] >= sigma_cutoff:
#             if rho[i] < rho.max() / 100.0:
#                 plt.scatter(rho[i], sigma[i], s=20, marker='o', c="black", edgecolor='face')
#             else:
#                 plt.scatter(rho[i], sigma[i], s=20, marker='o', c="C0", edgecolor='face')
#         else:
#             plt.scatter(rho[i], sigma[i], s=20, marker='o', c="C1", edgecolor='face')
#
#     plt.fill_between(np.array([-max(rho), max(rho) + 0.25]), np.array([sigma_cutoff, sigma_cutoff]),
#                      color="C1", alpha=0.1)
#
#     plt.xlim(0.0, max(rho) + 0.25)
#     plt.ylim(0.0, max(sigma) + 0.1)
#
#     plt.xlabel(r"$\rho$", fontsize=20)
#     plt.ylabel(r"$\sigma$", fontsize=20)
#
#     plt.tight_layout()
#     plt.savefig(path, dpi=300)
#     plt.close('all')
#
#
# # noinspection PyPep8Naming
# def FSFDP(dmat: Union[pd.DataFrame, np.ndarray],
#           kernel: str = "gaussian",
#           d_c: Union[str, float] = "auto",
#           d_c_neighbors_fraction: float = 0.02,
#           sigma_cutoff: Union[bool, float] = False):
#     """
#     Simplified FSFDP algorithm. Instead of halo, the distance of crystals from center is printed in the output to check
#     possible errors.
#     :param dmat: Distance Matrix, expressed as a pandas DataFrame or Numpy array. If an indexed DataFrame is used,
#                  results are shown using structures' IDs
#     :param kernel: Kernel function to calculate the distance, it can be 'cutoff' or 'gaussian'
#     :param d_c: Distance cutoff used to calculate the density (rho)
#     :param d_c_neighbors_fraction: Average number of neighbors with respect to total used to calculate d_c
#     :param sigma_cutoff: Sigma cutoff for the decision graph. If false you can select it from the plot.
#     :return:
#     """
#
#     if isinstance(dmat, np.ndarray):
#         dmat = pd.DataFrame(dmat)
#
#     if d_c == "auto":
#         d_c = np.sort(dmat.values.flatten())[int(dmat.values.size * d_c_neighbors_fraction) + dmat.values.shape[0]]
#
#     # Find density vector
#     rho = np.zeros(dmat.values.shape[0])
#     if kernel == "gaussian":
#         def kernel_function(d_ij):
#             return np.exp(-(d_ij / d_c) * (d_ij / d_c))
#     elif kernel == "cutoff":
#         def kernel_function(d_ij):
#             return 1 if d_ij < d_c else 0
#     else:
#         def kernel_function(d_ij):
#             return np.exp(-(d_ij / d_c) * (d_ij / d_c))
#
#         print("Kernel Function not recognized, switching to 'gaussian'")
#
#     for i in range(dmat.values.shape[0] - 1):
#         for j in range(i + 1, dmat.values.shape[0]):
#             rho[i] += kernel_function(dmat.values[i][j])
#             rho[j] += kernel_function(dmat.values[i][j])
#
#     rho = pd.Series(rho, index=dmat.index, name="rho")
#
#     # Find sigma vector
#     sigma = pd.Series(np.full(rho.shape, -1.0), dmat.index, name="sigma")
#     nn = pd.Series(np.full(rho.shape, pd.NA), dmat.index, dtype="string", name="NN")
#     for i in sigma.index:
#         if rho[i] == np.max(rho.values):
#             continue
#         else:
#             sigma[i] = np.nanmin(np.where(rho > rho[i], dmat[i].values, np.nan))
#             nn[i] = str(dmat.index[np.nanargmin(np.where(rho > rho[i], dmat[i].values, np.nan))])
#     sigma[rho.idxmax()] = np.nanmax(sigma.values)
#
#     # plot results
#     if not sigma_cutoff:
#         sigma_cutoff = _decision_graph(rho, sigma)
#
#     # Assign structures to cluster centers
#     dataset = pd.concat((rho, sigma, nn,
#                          pd.Series(np.full(rho.shape, pd.NA), dmat.index, name="cluster"),
#                          pd.Series(np.full(rho.shape, pd.NA), dmat.index, name="distance")),
#                         axis=1).sort_values(by="rho", ascending=False)
#
#     for i in dataset.index:
#         if dataset.loc[i, "sigma"] >= sigma_cutoff or i == dataset.index[0]:
#             dataset.at[i, "cluster"] = i
#             dataset.at[i, "distance"] = 0.0
#
#         else:
#             dataset.at[i, "cluster"] = dataset.loc[dataset.loc[i]["NN"]]["cluster"]
#             dataset.at[i, "distance"] = dmat.loc[i, dataset.loc[i, "cluster"]]
#
#     return dataset, sigma_cutoff
