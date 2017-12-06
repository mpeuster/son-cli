import os
import sys
import subprocess
import shutil
import time
import yaml
import logging

MAX_VNF = 3
REPETITIONS = 2


def read_yaml(path):
    yml = None
    with open(path, "r") as f:
            try:
                yml = yaml.load(f)
            except yaml.YAMLError as ex:
                logging.exception("YAML error while reading %r." % path)
    return yml


def write_yaml(path, data):
    with open(path, "w") as f:
        try:
            yaml.dump(data, f, default_flow_style=False)
        except yaml.YAMLError as ex:
            logging.exception("YAML error while writing %r" % path)


def clear_temp(path="son_temp"):
    print("clear temp")
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)


def copy_project(src="son-ns-template", dst="son_temp/son-ns"):
    print("copy project")
    shutil.copytree(src, dst)
    

def add_vnf_to_project(vnf_id):
    print("add vnf")
    # 1. read existing vnfd
    vnfd = read_yaml("son_temp/son-ns/sources/vnf/vnf1/vnfd-vnf1.yml")
    # 2. read existing nsd
    nsd = read_yaml("son_temp/son-ns/sources/nsd/nsd-sample.yml")
    # 3. create vnf folder
    os.makedirs("son_temp/son-ns/sources/vnf/vnf{}".format(vnf_id))
    # 4. update vnfd
    vnfd["name"] = "vnf{}".format(vnf_id)
    # 5. update nsd
    nsd["network_functions"].append({
        "vnf_id": "vnf{}".format(vnf_id),
        "vnf_vendor": "eu.sonata-nfv",
        "vnf_name": "vnf{}".format(vnf_id),
        "vnf_version": "0.1"
    })
    # 6. write vnfd
    write_yaml("son_temp/son-ns/sources/vnf/vnf{}/vnfd-vnf{}.yml".format(vnf_id, vnf_id), vnfd)
    # 7. write nsd
    write_yaml("son_temp/son-ns/sources/nsd/nsd-sample.yml", nsd)


def package_project():
    print("package project")
    t_start = time.time()
    subprocess.call("cd son_temp; son-package --project son-ns", shell=True)
    return abs(time.time() - t_start)

    
def run():
    results = list()
    clear_temp()
    copy_project()

    for n in range(1, MAX_VNF + 1):
        if n > 1:
            # add a VNF for next run
            add_vnf_to_project(n)
        for r in range(0, REPETITIONS):
            t = package_project()
            results.append({"n_vnf": n,
                            "r_id": r,
                            "t_pack_service": t,
                            "t_pack_vnfs": 0.0})
    clear_temp()
    return results


def main():
    # only for testing
    #clear_temp()
    #copy_project()
    #add_vnf_to_project(2)
    #package_project()
    #return
    print(run())
    

if __name__ == '__main__':
    main()

