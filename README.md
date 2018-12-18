# SIF (Python)

Sif Python (sif) is the Python API for working with the Singularity SIF image
format. This library is under development! The basic functionality so far is to 
parse the header, only using Python:

```
boxes.simg is a SIF file.
SIF Header version 01
SIF Header arch 02
SIF Header uuid 0eae46df-1975-e44c-888b-8b9915f87f52
SIF Header ctime 1544537033
SIF Header mtime 1544537033
SIF Header dfree 46
SIF Header dtotal 48
SIF Header descroff 4096
SIF Header descrlen 28080
SIF Header dataoff 32768
SIF Header datalen 196952064

Architecture: AMD64 arch code

Deffile Datatype 16385
Deffile Used True
Deffile ID 1
Deffile Groupid 4026531841
Deffile Link 0
Deffile Fileoff 32768
Deffile Filelen 39
Deffile Storelen 39
Deffile Ctime 1544537033
Deffile Mtime 1544537033
Deffile UID 0
Deffile Gid 0
Deffile name .
Deffile extra 

Partition Datatype 16388
Partition Used True
Partition ID 2
Partition Groupid 4026531841
Partition Link 0
Partition Fileoff 36864
Partition Filelen 196947968
Partition Storelen 196952025
Partition Ctime 1544537033
Partition Mtime 1544537033
Partition UID 0
Partition Gid 0
Partition name squashfs-955608129.img
Partition fstype 1
Partition partype 2
Partition extra 02
<SIF:boxes.simg>
```



## Usage

By default, the SIF header version provided is the most up to date with Singularity.
If you need to specify a particular header, set the environment variable for it:

```bash
SIF_VERSION="02"
export SIF_VERSION
```

### Python
In Python, you will likely want to start with an image, and load it for inspection.
The client will quickly tell you if it's a SIF header or not based on the `SIF_MAGIC`
after the interpreter line:

**This is a SIF image**

```python
image = 'salad.simg'
from sif.main import SIFHeader
header = SIFHeader(image)

boxes.simg is a SIF file.
Architecture: AMD64 arch code
Found SIF version 01
Found SIF arch 02
```

You don't have to load the header right away:

```python
header = SIFHeader('boxes.simg', load=False)
boxes.simg is a SIF file.

header.load_header()

Architecture: AMD64 arch code
Found SIF version 01
Found SIF arch 02
```

**This is not a SIF image**

```python
image = 'salad.simg'
from sif.main import SIFHeader
header = SIFHeader(image)
...
ERROR salad.simg is not a SIF file.
```

## Licenses

This code is licensed under the Affero GPL, version 3.0 or later [LICENSE](LICENSE).
The SIF Header format is licesed by [Sylabs](https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go).
