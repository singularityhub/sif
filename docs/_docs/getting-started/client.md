---
title: SIF Python Client
category: Getting Started
order: 2
---

SIF Python provides a command line executable to easily give you access to a
Python shell with your container loaded. After you [install]({{ site.url }}{{ site.baseurl }}/install/)
SIF Python, you can see the client with the command line executable "sif":

```bash
$ sif


SIF Python v0.0.11
usage: sif [-h] [--debug] [--quiet] [--version] {shell} ...

SIF Python

optional arguments:
  -h, --help  show this help message and exit
  --debug     use verbose logging to debug.
  --quiet     show SIF Python verison and exit
  --version   suppress additional output.

actions:
  actions for SIF Python

  {shell}     sif python actions
    shell     shell into a session a client.
```

## Version

To see the version:

```bash
$ sif --version
0.0.11
```


## Shell

The purpose of SIF Python is to give an interactive Python shell, and so the
client is currently optimized to do this. You can provide the SIF container
as the first argument to get an interactive shell.

```bash
$ sif shell boxes.simg

boxes.simg is a SIF file.
SIF Header version 01
SIF Header arch 02
SIF Header uuid 0eae46df-1975-e44c-888b-8b9915f87f52
...
Python 3.6.4 |Anaconda custom (64-bit)| (default, Jan 16 2018, 18:10:19) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.2.1 -- An enhanced Interactive Python. Type '?' for help.

```

You get loaded for you the `header`, and are provided with your original
image name under the variable `image` along with the `SIFHeader` class:

```python
In [1]: header
Out[1]: <SIF:boxes.simg>

In [2]: image
Out[2]: 'boxes.simg'

In [3]: SIFHeader
Out[3]: sif.main.header.SIFHeader
```

Let's look at our header! The chunk of content you are interested in
are within the descriptor blocks. You'll again see sections for the 
header, definition file, partition, and signature (if present). 
You can inspect each of these in more
detail by looking at the defs dictionary:

```python
header.desc.keys()
dict_keys(['deffile', 'partition', 'signature'])
```

Here is the signature block, for example:

```python
header.desc['signature']
{'Ctime': 1546726508,
 'Datatype': 16389,
 'Filelen': 955,
 'Fileoff': 196984832,
 'Gid': 0,
 'Groupid': 4026531841,
 'ID': 3,
 'Link': 2,
 'Mtime': 1546726508,
 'Storelen': 955,
 'UID': 0,
 'Used': True,
 'hastype': 2,
 'name': 'part-signature',
 'publicKey': '-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA256\n\nSIFHASH...
...}
```

The header metadata is under the meta attribute:

```python
> header.meta
{'arch': '02',
 'ctime': 1544537033,
 'datalen': 196953019,
 'dataoff': 32768,
 'descrlen': 28080,
 'descroff': 4096,
 'dfree': 45,
 'dtotal': 48,
 'mtime': 1546726508,
 'uuid': '0eae46df-1975-e44c-888b-8b9915f87f52',
 'version': '01'}
```

There is also a function to easily get the definition file (also a part of header.desc['deffile'])

```python
> header.print_deffile()
bootstrap: docker
from: vanessa/boxes
```

If you have any questions or issues, please [open an issue]({{ site.repo }}/issues)!
SIF Python is a new library and its development will be driven by the needs
of its users.
