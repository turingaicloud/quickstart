# Turing AI Cloud Quick Start
## Workflow Overview

![Workflow](./static/workflow.png)

The above picture illustrates the submission and debug workflows of TACC job.

## Upload SSH public key to TACC
Before using tcloud SDK, please make sure that you have submitted your public key to TACC. You may generate SSH public key according to the [steps](https://git-scm.com/book/en/v2/Git-on-the-Server-Generating-Your-SSH-Public-Key).

## Download/Install tcloud SDK
- __Download tcloud SDK__ \
Download the latest tcloud SDK from [tags](https://github.com/turingaicloud/quickstart/tags).
- __Install tcloud SDK__ \
Place `setup.sh` and `tcloud` in the same directory, and run `setup.sh`.

## Configuration
### CLI Configuration
1. Before using the tcloud CLI to submit ML jobs, you need to configure your TACC credentials. You can do this by running the `tcloud config` command:
```
$ tcloud config [-u/--username] MYUSERNAME
$ tcloud config [-f/--file] MYPRIVATEFILEPATH
```
2. You need to run `tcloud init` command to obtain the latest cluster hardware information from TACC cluster.

### Job Configuration
#### TUXIV.CONF

You can use `tcloud init` to pull the latest cluster configuration from TACC. There are four parts in `tuxiv.conf` that configure different parts of job submission. Noted that `tuxiv.conf` follows **yaml format**.

+ Entrypoint

  In this section, you should input you shell commands to run your code line-by-line. The tcloud CLI will help run the job according to your commands.

  ~~~yaml
  entrypoint:
      - python ${TACC_WORKDIR}/mnist.py --epoch=3 
  ~~~

+ Environment

  In this section, you can specify your software requirements, including the environment name, dependencies, source channels and so on. The tcloud CLI will help build your environment with *miniconda*.

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

  **Note:** You can modify the output log path in Job section. For debugging purpose, we recommend you set the `output` value under `${TACC_USERDIR}` directory and check it using `tcloud ls` and `tcloud download`.

+ Datasets
  - tcloud will help place the public datasets access in `TACC_USERDIR`. You can view the table of  datasets at [Dataset Info](https://docs.google.com/spreadsheets/d/18qi2YpYvuXkWns7KY9pHYQclhS1Yyt5ysqgZ4plYcTg/edit#gid=0) or check the table below.

      - 
        |  | Dataset Name |
        | :------: | :------: |
        | 0 | imagenet |
        | 1 | mnist |
        | 2 | cifar-10 |
        | 3 | coco17 |
        | 4 | more datasets upon request |

    - to access the public dataset you need to add this command in your tuxiv.conf file:
      ~~~yaml
      datasets:
        - imagenet
      ~~~
    - also use this path as a dataset directory:
      ~~~shell
      ${TACC_USERDIR}/DATASET_NAME
      ~~~
  - User dataset: if you want to use your own dataset, you may **skip** this part and follow the [instructions](docs/user_dataset.md) to upload and use your dataset.


#### TACC VARIABLES

+ `TACC_WORKDIR`: TACC job workspace directory. Each job has a different workspace directory.
+ `TACC_USERDIR`: TACC User directory.
+ `TACC_SLURM_USERLOG`: Slurm log directory. The default value is `${TACC_USERDIR}/slurm_log`.

## Job Monitoring
In this section, we provide two methods to monitor the job log.
+ Download

  You can either save your output files in `USERDIR` or copy your output files to `USERDIR` in your own code. After training, you can use `tcloud ls [filepath]` to find the output files and use `tcloud download [filepath]`. Note that you can only read and download files in `USERDIR`, and the files in `WORKDIR` may be removed after the job is finished.
  
+ Run application services

  Here we give an example of application service, which uses tensorboard to monitor a job. 
  ~~~shell
  ssh -p 30041 -L 10006:127.0.0.1:10006  username@ising.cse.ust.hk /mnt/home/username/.Miniconda3/envs/torch-env/bin/tensorboard --logdir=/mnt/home/username/WORKDIR/PyTorch/runs --port=10006
  ~~~
## Demo video
The following videos will help you use tcloud CLI to begin your TACC journey: [demo video](https://drive.google.com/file/d/1eEZzgH3MipdXy3eIfgasUaMdlMquCqf8/view?usp=sharing) and [conda-cache video](https://drive.google.com/file/d/1hfFfWZoJj6dlNiOK-dbyvrE_VmM07w7A/view?usp=sharing).

## Examples
Basic examples are provided under the [example](example) folder. These examples include: [HelloWorld](example/helloworld), [TensorFlow](example/TensorFlow), [PyTorch](example/PyTorch) and [MXNet](example/MXNet).
