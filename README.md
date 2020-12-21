# TACC Quick Start
## Workflow Overview

![Workflow](./static/workflow.png)

The above picture illustrates TACC job submitting and debugging workflow.

## Download/Install tcloud SDK
- __Download tcloud SDK__ \
Download the latest tcloud SDK from [tags](https://github.com/turingaicloud/quickstart/tags).
- __Install tcloud SDK__ \
Place `setup.sh` and `tcloud` in the same directory, and run `setup.sh`.

## Configuration
### CLI Configuration
1. Before using the tcloud CLI and submit ML jobs to TACC, you need to configure your TACC credentials. You can do this by running the `tcloud config` command:
```
$ tcloud config [-u/--username] MYUSERNAME
$ tcloud config [-f/--file] MYPRIVATEFILEPATH
```
2. You need to run `tcloud init` command to obtain the latest cluster hardware information from TACC cluster.

### Job Configuration
#### TUXIV.CONF

You can use `tcloud init` to pull the latest cluster configurations from remote. There are four parts in `tuxiv.conf`, config different parts of job submission. Noted that `tuxiv.conf` follows the yaml format.

+ Entrypoint

  In this section, you should insert you shell commands to run your code line-by-line. The tcloud CLI will run the job as your configurations.

  ~~~yaml
  entrypoint:
      - python ${TACC_WORKDIR}/mnist.py --epoch=3
  ~~~

+ Environment

  In this section, you can specify your conda configurations for virtual environment used in the cluster, including environment name, dependencies, source channels and so on.

  ~~~yaml
  environment:
      name: torch-env
      dependencies:
          - pytorch=1.6.0
          - torchvision=0.7.0
      channels: pytorch
  ~~~

+ Job

  In this section, you can specify your slurm configurations for slurm cluster resources, including number of nodes, CPUs, GPUs, output file and so on. All the slurm cluster configuration should be set in the general part.

  ~~~yaml
  job:
      name: test
      general:
          - nodes=2
          - output=${TACC_SLURM_USERLOG}/output.log
  ~~~

+ Datasets

  In this section, you can specify the needed CityNet dataset name, and tcloud will help place the dataset access in `TACC_USERDIR`. You can view the table of CityNet datasets at [CityNet Dataset Info](https://docs.google.com/spreadsheets/d/18qi2YpYvuXkWns7KY9pHYQclhS1Yyt5ysqgZ4plYcTg/edit#gid=0).

  ~~~yaml
  datasets:
    - OpenRoadMap
  ~~~

## TACC VARIABLES

+ `TACC_WORKDIR`: TACC job workspace directory, each job has a different workspace directory.
+ `TACC_USERDIR`: TACC User directory.
+ `TACC_SLURM_USERLOG`: Slurm log directory, the default value is `${TACC_USERDIR}/slurm_log`.

## Job Monitoring
In this section, we provide two different methods to monitoring a job log and other outputs.
+ Download

  You can either save your output file in the `USERDIR` or copy your output file to the `USERDIR` in your own code. After training you can use `tcloud ls [filepath]` to find the output file and use `tcloud download [filepath]`. Noted that you can only read and download the file in the `USERDIR`, and the file in `WORKDIR` may be remove after the job is terminated.
  
+ Run application services

  Here we give an example of application service, using tensorboard to monitor the job. 
  ~~~shell
  ssh -p 30041 -L 10006:127.0.0.1:10006  username@sing.cse.ust.hk /mnt/sharefs/home/username/.Miniconda3/envs/torch-env/bin/tensorboard --logdir=/mnt/sharefs/home/username/WORKDIR/PyTorch/runs --port=10006
  ~~~
## Demo video
You can find the demo video at [video](https://drive.google.com/file/d/1eEZzgH3MipdXy3eIfgasUaMdlMquCqf8/view?usp=sharing).

## Examples
Basic examples are provided under the [example](example) folder. These examples include: [HelloWorld](example/helloworld), [TensorFlow](example/TensorFlow), [PyTorch](example/PyTorch) and [MXNet](example/MXNet).
