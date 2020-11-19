from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import tensorflow as tf
import re
import os

def tf_config_from_slurm(ps_number, port_number=12222):
    """
    Creates configuration for a distributed tensorflow session 
    from environment variables  provided by the Slurm cluster
    management system.
    
    @param: ps_number number of parameter servers to run
    @param: port_number port number to be used for communication
    @return: a tuple containing cluster with fields cluster_spec,
             task_name and task_id 
    """
    
    nodelist = os.environ["SLURM_JOB_NODELIST"]
    nodename = os.environ["SLURMD_NODENAME"]
    nodelist = _expand_nodelist(nodelist)
    num_nodes = int(os.getenv("SLURM_JOB_NUM_NODES"))
    
    if len(nodelist) != num_nodes:
        raise ValueError("Number of slurm nodes {} not equal to {}".format(len(nodelist), num_nodes))
    
    if nodename not in nodelist:
        raise ValueError("Nodename({}) not in nodelist({}). This should not happen! ".format(nodename,nodelist))
    
    ps_nodes = [node for i, node in enumerate(nodelist) if i < ps_number]
    worker_nodes = [node for i, node in enumerate(nodelist) if i >= ps_number]
    
    if nodename in ps_nodes:
        my_job_name = "ps"
        my_task_index = ps_nodes.index(nodename)
    else:
        my_job_name = "worker"
        my_task_index = worker_nodes.index(nodename)
    
    worker_sockets = [":".join([node, str(port_number)]) for node in worker_nodes]
    ps_sockets = [":".join([node, str(port_number)]) for node in ps_nodes]
    cluster = {"worker": worker_sockets, "ps" : ps_sockets}
    return cluster, my_job_name, my_task_index

def _pad_zeros(iterable, length):
    return (str(t).rjust(length, '0') for t in iterable)
    
def _expand_ids(ids):
    ids = ids.split(',')
    result = []
    for id in ids:
        if '-' in id:
            begin, end = [int(token) for token in id.split('-')]
            result.extend(_pad_zeros(range(begin, end+1), len(id.split('-')[0])))
            # print(begin, end)
        else:
            result.append(id)
        # result.append(id)
    return result

def _expand_nodelist(nodelist):
    prefix, ids = re.findall("(.*)\[(.*)\]", nodelist)[0]
    ids = _expand_ids(ids)
    result = [prefix + str(id) for id in ids]
    return result

def _worker_task_id(nodelist, nodename):
    return nodelist.index(nodename)
