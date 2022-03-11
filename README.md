# Turing AI Cloud Quick Start
## Workflow Overview

![Workflow](./static/workflow.png)

The above picture illustrates the submission and debug workflows of TACC job.

## Creating a TACC account
Before using tcloud SDK, please make sure that you have applied for a TACC account and submitted your public key to TACC. You may generate SSH public key according to the [steps](https://git-scm.com/book/en/v2/Git-on-the-Server-Generating-Your-SSH-Public-Key).
To apply for a TACC account, please visit [our website ](https://turing.ust.hk/).

## Installing `tcloud` SDK
- __Download tcloud SDK__ \
Download the latest tcloud SDK from [tags](https://github.com/turingaicloud/quickstart/tags).
- __Install tcloud SDK__ \
Place `setup.sh` and `tcloud` in the same directory, and run `setup.sh`.

## Submitting Your First TACC Job
### CLI Tool Initialization
+ 
  First, you need to configure your TACC credentials. You can do this by running the `tcloud config` command:
  ```
  $ tcloud config [-u/--username] MYUSERNAME
  $ tcloud config [-f/--file] MYPRIVATEFILEPATH
  ```
+ 
  Then, run `tcloud init` command to obtain the latest cluster hardware information from TACC cluster.
  ```
  PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
  tacc*        up   infinite      5  alloc 10-0-7-[18-19],10-0-8-[18-19]
  tacc*        up   infinite     19   idle 10-0-2-[18-19],10-0-3-[10-13]
  ```

### Download Sample Job
You can use [this link](https://github.com/turingaicloud/quickstart/archive/refs/heads/master.zip) to download our example code.


### Submit a Job
Each job requires a `main.py` with `tuxiv.conf`

+
  main.py: Your machine learning training code.

+
  tuxiv.conf: [Detail about tuxiv.conf](tuxiv.conf.md)

  
After tcloud is configured correctly, you can try to submit your first job. 

1. Go to the example folder in your terminal.
2. Run `tcloud submit` command.
    ```
    ~/Dow/quickstart-master/example/helloworld ❯ tcloud submit
    Start parsing tuxiv.conf...
    building file list ...
    8 files to consider
    helloworld/
    helloworld/run.sh
            151 100%    0.00kB/s    0:00:00 (xfer#1, to-check=5/8)
    helloworld/configurations/
    helloworld/configurations/citynet.sh
              12 100%   11.72kB/s    0:00:00 (xfer#2, to-check=2/8)
    helloworld/configurations/conda.yaml
            107 100%  104.49kB/s    0:00:00 (xfer#3, to-check=1/8)
    helloworld/configurations/run.slurm
            278 100%  271.48kB/s    0:00:00 (xfer#4, to-check=0/8)

    sent 429 bytes  received 144 bytes  382.00 bytes/sec
    total size is 1071  speedup is 1.87
    Submitted batch job 2000
    Job helloworld submitted.
    ```

### Retrive Your Job Status and Output
In this section, we provide two methods to monitor the job log.

After training, you can use `tcloud ls [filepath]` to find the output files
+ cat

  You can configure your log path in the `tuxiv.conf`. The default path is `slurm_log/slurm-jobid.out`.

  ```
  tcloud cat slurm_log/slurm-jobid.out
  ```
  In the helloworld example, the [tuxiv.conf](example/helloworld/tuxiv.conf) file specifies the log path as `slurm_log/hello.log`


+ download

  You can use `tcloud download [filepath]`. 
  
  Note that you can only read and download files in `USERDIR`, and the files in `WORKDIR` may be removed after the job is finished.
  ```
  tcloud download slurm_log/slurm-jobid.out
  ```

### Manage your environment
+ Reuse environment
  
  We offer two methods to environmental management.
  1. If you don't have the name section under the environment block in tuxiv.conf, tcloud will create a new environment for your new project.

  2. You can add the environment name in `tuxiv.conf` to reuse an existing environment. [Detail about tuxiv.conf](tuxiv.conf.md)


## Demo video
The following videos will help you use tcloud CLI to begin your TACC journey: [demo video](https://hkustconnect-my.sharepoint.com/:v:/g/personal/dsunak_connect_ust_hk/EUYW3f8IRwVLhBtCYP_ufs4BpQ7CaxrCUBiUexY7-nLX7w?e=O2gR2G).

## Examples
Basic examples are provided under the [example](example) folder. These examples include: [HelloWorld](example/helloworld), [TensorFlow](example/TensorFlow), [PyTorch](example/PyTorch) and [MXNet](example/MXNet).

## FAQ
[FAQ](FAQ.md)