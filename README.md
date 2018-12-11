# SIF (Python)

Sif Python (sif) is the Python API for working with the Singularity SIF image
format. This library is under development. 

[![asciicast](https://asciinema.org/a/216447.svg)](https://asciinema.org/a/216447?speed=2)

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
