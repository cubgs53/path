#!/usr/bin/env python

import os, re, csv

def check(name):
    for file_name in os.listdir(os.getcwd()):
        if re.match('{}.o[0-9]+'.format("omp"), file_name):
            print file_name
            omp_out = open(file_name, 'r')
            omp_result = {}
            found = 0
            for line in omp_out:
                par = line.split()
                if found == 0 and len(par) > 0 and par[0] == '==':
                    found = 1
                    p = par[2]
                elif found == 1 and len(par) > 0 and par[0] == 'n:':
                    found = 2
                    n = par[-1]
                elif found == 2 and len(par) > 0 and par[0] == 'Check:':
                    result = par[-1]
                    found = 0
                    omp_result[n] = result
            omp_out.close()

    for file_name in os.listdir(os.getcwd()):
        if re.match('{}.o[0-9]+'.format(name), file_name):
            print file_name
            new_out = open(file_name, 'r')
            found = 0
            for line in omp_out:
                par = line.split()
                if found == 0 and len(par) > 0 and par[0] == '==':
                    found = 1
                    p = par[2]
                elif found == 1 and len(par) > 0 and par[0] == 'n:':
                    found = 2
                    n = par[-1]
                elif found == 2 and len(par) > 0 and par[0] == 'Check:':
                    result = par[-1]
                    found = 0
                    if result != omp_result[n]:
                        print "ERROR"
                        print "omp result: %d, %s" %(n, omp_result[n])
                        print "%s result: %d, %s" %(name, n, result)
            new_out.close()

check('omp')
check('mpi')
check('hybrid')
