#### ENVIRONMENT VARIABLES

+ `TACC_WORKDIR`: TACC job workspace directory. Each job has a different workspace directory.
+ `TACC_USERDIR`: TACC User directory.
+ `TACC_SLURM_USERLOG`: Slurm log directory. The default value is `${TACC_USERDIR}/slurm_log`.
- tip: These ENVIRONMENT VARIABLES can be used in `tuxiv.conf` or read in `python` code.

There are four parts in `tuxiv.conf` that configure different parts of job submission. Noted that `tuxiv.conf` follows **yaml format**.

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

  In this section, you can specify your configurations for cluster resources, including number of nodes, CPUs, GPUs, output file and so on. All the cluster configuration should be set in the general part.

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

  