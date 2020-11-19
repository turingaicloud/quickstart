# TCloud Examples

TACC support multiple ML frameworks such as TensorFlow, PyTorch and MXNet. We will later support some specialized ML framework like FATE, etc. Here we list several job examples of different frameworks.

## TensorFlow

+ Dataset: mnist
+ Task: image classification
+ Code: [mnist.py](https://github.com/xcwanAndy/tcloud-sdk/blob/master/example/TensorFlow/mnist.py)

### Getting started

+ Install tcloud CLI, and run `tcloud init` to generate template for configuration.

+ Configuration

  + Config user informations using `tcloud config`.

  + TACC ENV

    ~~~shell
    TACC_WORKERDIR #repo directory
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

+ Enter the `TACC_WORKDIR` directory and follow the steps.
+ Build environment and submit job: `tcloud submit`
+ Monitor job: `tcloud ps [job id]`
+ Cancel job: `tcloud cancel [job id]`



## PyTorch

+ Dataset: mnist
+ Task: image classification
+ Code: [mnist.py](https://github.com/xcwanAndy/tcloud-sdk/blob/master/example/Pytorch/mnist.py)

### Getting started

+ Install tcloud CLI, and run `tcloud init` to generate template for configuration.

+ Configuration

  + Config user informations using `tcloud config`.

  + TACC ENV

    ~~~shell
    TACC_WORKERDIR #repo directory
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

+ Enter the `TACC_WORKDIR` directory and follow the steps.
+ Build environment and submit job: `tcloud submit`
+ Monitor job: `tcloud ps [job id]`
+ Cancel job: `tcloud cancel [job id]`



## MXNet

+ Dataset: mnist
+ Task: image classification
+ Code: [mnist.py](https://github.com/xcwanAndy/tcloud-sdk/blob/master/example/MXNET/mnist.py)

### Getting started

+ Install tcloud CLI, and run `tcloud init` to generate template for configuration.

+ Configuration

  + Config user informations using `tcloud config`.

  + TACC ENV

    ~~~shell
    TACC_WORKERDIR #repo directory
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

+ Enter the `TACC_WORKDIR` directory and follow the steps.
+ Build environment and submit job: `tcloud submit`
+ Monitor job: `tcloud ps [job id]`
+ Cancel job: `tcloud cancel [job id]`
