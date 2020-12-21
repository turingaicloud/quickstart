# Tcloud Examples

TACC supports multiple ML frameworks such as TensorFlow, PyTorch and MXNet. We will later support some specialized ML framework like FATE, etc. Here we list several job examples of different frameworks.

## HelloWorld

+ CityNet Dataset: OpenRoadMap
+ Task: basic usage of tcloud
+ Code: [main.py](helloworld/main.py)

### Getting started

+ Install tcloud CLI, and run `tcloud init` to pull the latest cluster configurations from remote.

+ Configuration

  + Configure user information using `tcloud config`.

  + TACC ENV

    ~~~shell
    TACC_WORKDIR # default repo directory
    TACC_USERDIR # user directory
    TACC_SLURM_USERLOG # slurm log directory default: ${TACC_USERDIR}/slurm_log
    ~~~

  + TuXiv configuration

    ~~~yaml
    # tuxiv.conf
    entrypoint:
    - python ${TACC_WORKDIR}/main.py
    environment:
        name: hello 
        dependencies:
            - python=3.6.9
    job:
        name: test
        general:
            - output=${TACC_SLURM_USERLOG}/hello.out
            - nodes=1
            - ntasks=1
            - cpus-per-task=1
    datasets:
      - OpenRoadMap
    ~~~

  + Model code modification

    ~~~python
    import os
    import shutil
    # get variables from env
    WORKDIR = os.environ.get('TACC_WORKDIR')
    USERDIR = os.environ.get('TACC_USERDIR')
    # show the directory tree
    os.system('tree -L 2 {}'.format(USERDIR))
    # basic copy operation
    shutil.copytree(WORKDIR, "{}/helloworld".format(USERDIR))
    ~~~

### Submit job

+ Enter the `helloworld` directory and follow the following steps.
+ Build environment and submit job: `tcloud submit`
+ Monitor job: `tcloud ps [-j] [<JOB_ID>]`
+ Obtain log: `tcloud download helloworld/slurm_log/hello.out`
+ Cancel job: `tcloud cancel [-j] [<JOB_ID>]`
+ View UserDir: `tcloud ls <PATH>`



## TensorFlow

+ Dataset: mnist
+ Task: image classification
+ Code: [mnist.py](TensorFlow/mnist.py)

### Getting started

+ Install tcloud CLI, and run `tcloud init` to pull cluster configurations from remote.

+ Configuration

  + Config user informations using `tcloud config`.

  + TACC ENV

    ~~~shell
    TACC_WORKDIR # default repo directory
    TACC_USERDIR # user directory
    TACC_SLURM_USERLOG # slurm log directory default: ${TACC_USERDIR}/slurm_log
    ~~~

  + TuXiv configuration
  
    ~~~yaml
    # tuxiv.conf
    entrypoint:
        - python ${TACC_WORKDIR}/mnist.py 
        - --task_index=0
        - --data_dir=${TACC_WORKDIR}/datasets/mnist_data
        - --batch_size=1
    environment:
        name: tf 
        dependencies:
            - tensorflow=1.15
    job:
        name: mnist
        general:
          - nodes=2
    ~~~

  + Model code modification
  
    Use ` tf.distribute.cluster_resolver.SlurmClusterResolver`  instead of other resolvers.

### Training

+ Enter the `TensorFlow` directory and follow the following steps.
+ Build environment and submit job: `tcloud submit`
+ Monitor job: `tcloud ps [-j] [<JOB_ID>]`
+ Cancel job: `tcloud cancel [-j] [<JOB_ID>]`
+ View UserDir: `tcloud ls <PATH>`



## PyTorch

+ Dataset: mnist
+ Task: image classification
+ Code: [mnist.py](PyTorch/mnist.py)

### Getting started

+ Install tcloud CLI, and run `tcloud init` to pull cluster configurations from remote.

+ Configuration

  + Config user informations using `tcloud config`.

  + TACC ENV

    ~~~shell
    TACC_WORKDIR # default repo directory
    TACC_USERDIR # user directory
    TACC_SLURM_USERLOG # slurm log directory default: ${TACC_USERDIR}/slurm_log
    ~~~

  + TuXiv configuration
  
    ~~~yaml
    # tuxiv.conf
    entrypoint:
        - python ${TACC_WORKDIR}/mnist.py --epoch=3
    environment:
        name: torch-env
        dependencies:
            - pytorch=1.6.0
            - torchvision=0.7.0
        channels: pytorch
    job:
        name: test
        general:
          - nodes=2
    ~~~

  + Model code modification

    Obtain environment variables from slurm cluster, and set the parameters for initialize the cluster.
  
    ~~~python
    # example
    def dist_init(host_addr, rank, local_rank, world_size, port=23456):
        host_addr_full = 'tcp://' + host_addr + ':' + str(port)
        torch.distributed.init_process_group("gloo", init_method=host_addr_full,
                                             rank=rank, world_size=world_size)
      assert torch.distributed.is_initialized()
    
    def get_ip(iplist):
        ip = iplist.split('[')[0] + iplist.split('[')[1].split('-')[0]
        
    rank = int(os.environ['SLURM_PROCID'])
    local_rank = int(os.environ['SLURM_LOCALID'])
    world_size = int(os.environ['SLURM_NTASKS'])
    iplist = os.environ['SLURM_STEP_NODELIST']
    ip = get_ip(iplist) # function get_ip() is depends on the format of nodelist 
    dist_init(ip, rank, local_rank, world_size)
    ~~~

### Training

+ Enter the `PyTorch` directory and follow the following steps.
+ Build environment and submit job: `tcloud submit`
+ Monitor job: `tcloud ps [-j] [<JOB_ID>]`
+ Cancel job: `tcloud cancel [-j] [<JOB_ID>]`
+ View UserDir: `tcloud ls <PATH>`



## MXNet

+ Dataset: mnist
+ Task: image classification
+ Code: [mnist.py](MXNet/mnist.py)

### Getting started

+ Install tcloud CLI, and run `tcloud init` to pull cluster configurations from remote.

+ Configuration

  + Config user informations using `tcloud config`.

  + TACC ENV

    ~~~shell
    TACC_WORKDIR # default repo directory
    TACC_USERDIR # user directory
    TACC_SLURM_USERLOG # slurm log directory default: ${TACC_USERDIR}/slurm_log
    ~~~

  + TuXiv configuration
  
    ~~~yaml
    # tuxiv.conf
    entrypoint:
    - python ${TACC_WORKDIR}/mnist.py
    environment:
        name: mxnet-env 
        dependencies:
            - mxnet=1.5.0
    job:
        name: test
        general:
          - nodes=2
    ~~~

  + Model code modification
  
    Obtain environment variables from slurm cluster, and set the parameters for initialize the cluster.

### Training

+ Enter the `MXNet` directory and follow the following steps.
+ Build environment and submit job: `tcloud submit`
+ Monitor job: `tcloud ps [-j] [<JOB_ID>]`
+ Cancel job: `tcloud cancel [-j] [<JOB_ID>]`
+ View UserDir: `tcloud ls <PATH>`

