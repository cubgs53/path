import os
import time

n= range(480,5100,480)
threads_mpi = range(1,25,1)
threads_omp = [1]

def create_pbs(name, threads, n, mpi=False):
    fname = "{}.pbs".format(name)
    out = open(fname,'w')
    s = '''#!/bin/sh -l
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

create_pbs("fw-hybrid", mpi=True, n=n, threads=threads_mpi)
create_pbs("fw-omp", mpi=False, n=n, threads=threads_omp)
create_pbs("fw-mpi", mpi=True, threads=threads_mpi, n=n)
create_pbs("rs-hybrid", mpi=True, n=n, threads=threads_mpi)
create_pbs("rs-omp", mpi=False, n=n, threads=threads_omp)
create_pbs("rs-mpi", mpi=True, threads=threads_mpi, n=n)
create_pbs("block-hybrid", mpi=True, n=n, threads=threads_mpi)
create_pbs("block-omp", mpi=False, n=n, threads=threads_omp)
create_pbs("block-mpi", mpi=True, threads=threads_mpi, n=n)
