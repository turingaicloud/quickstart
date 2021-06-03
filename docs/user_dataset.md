# Upload dataset
You may upload your dataset with `tcloud upload` command:
```
tcloud upload <local_dirpath> [<remote_dirpath>]
```
The `tcloud upload` command helps upload your dataset to ${TACC_USERDIR}.

# Specify dataset in code
After uploading your own dataset, you must add several codes to specify the location of the dataset. Below is an example in PyTorch:

~~~python
workdir = os.environ.get('TACC_WORKDIR')
userdir = os.environ.get('TACC_USERDIR')

...
train_dataset = torchvision.datasets.MNIST('{}/{}'.format(userdir, <YOUR_DATASET_PATH>), train=True, download=False,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ]))
train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset, num_replicas=world_size, rank=rank)
train_loader = torch.utils.data.DataLoader(
    train_dataset,
    batch_size=args.batch_size,
    sampler=train_sampler,
    **kwargs)
~~~