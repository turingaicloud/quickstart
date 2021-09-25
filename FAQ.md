# FAQ

### 1. How to use tcloud?
- It's easy to use. Try helloworld example first.
### 2. Can I use my own dataset?
- Of course, you can upload your dataset to a specific directory via tcloud upload.
### 3. What is the current tcloud strategy？
- Now, there are a total of 8 nodes in tacc, and each node has 4 GTX3090 and 40 CPU cores.
### 4. Can I ssh to the tcloud server?
- All users cannot ssh to our server. If you have special needs, please feel free to contact us.
### 5. Can I keep using tacc without running an experiment?
- Can not. We will regularly kill processes that occupy nodes for a long time but do not run experiments.
### 6. How to cancel a tcloud job?
- You can use `tcloud cancel -j [JOBID]` command.
### 7. Why did I submit a job but there is no log?
- It's hard to say. This is most likely an error generated before the job is assigned to tcloud to run. Please carefully check the tuxiv.conf file.