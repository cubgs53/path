#!/usr/bin/env python

import os
import time

n = [600 * k for k in range(1, 13) if 12 % k == 0]
threads_mpi = [k for k in range(1, 25) if 24 % k == 0]
threads_omp = [1]

def create_pbs(name, threads, n, mpi=False):
    fname = "{}.pbs".format(name)
    out = open(fname,'w')
    s = '''
#!/bin/sh -l
#PBS -l nodes=1:ppn=24
#PBS -l walltime=5:00:00
#PBS -N {}
#PBS -j oe
module load cs5220
cd $PBS_O_WORKDIR
'''.format(name)
    out.write(s)
    for t in threads:
        for ni in n:
            if mpi:
                line = "mpirun -n {} ../{}.x -n {}\n".format(t, name, ni)
            else:
                line = "../{}.x -n {}\n".format(name, ni)
            out.write(line)
    out.close()
    os.system("qsub {}".format(fname))

create_pbs("omp", mpi=False, n=n, threads=threads_mpi)
create_pbs("mpi", mpi=True, n=n, threads=threads_omp)
create_pbs("hybrid", mpi=True, n=n, threads=threads_mpi)
