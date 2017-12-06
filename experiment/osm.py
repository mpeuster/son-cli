import os
import sys
import subprocess
import shutil
import time
import yaml
import logging


def clear_temp(path="osm_temp"):
    print("clear temp")
    shutil.rmtree(path, ignore_errors=True)


def copy_project(src="osm-ns-template", dst="osm_temp"):
    print("copy project")
    shutil.copytree(src, dst)


def package_project(n_vnfs):
    print("package project")
    t_start = time.time()
    # package each VNF
    for i in range(n_vnfs):
        subprocess.call("cd osm_temp; ./generate_descriptor_pkg.sh -t vnfd -N http", shell=True)
    # package service descriptor
    subprocess.call("cd osm_temp; ./generate_descriptor_pkg.sh -t nsd -N demo_nsd", shell=True)
    return abs(time.time() - t_start)

    
def run(max_vnf=3, repetitions=2):
    results = list()
    clear_temp()
    copy_project()

    for n in range(1, max_vnf + 1):
        for r in range(0, repetitions):
            t = package_project(n)
            results.append({"project": "OSM",
                            "n_vnf": n,
                            "r_id": r,
                            "t_pack_service": t,
                            "t_pack_vnfs": 0.0})
    clear_temp()
    return results


def main():
    # only for testing
    #clear_temp()
    #copy_project()
    #package_project(2)
    #return
    print(run())
    

if __name__ == '__main__':
    main()

