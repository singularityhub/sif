---
title: Welcome
permalink: /
---

**Singularity Image Format (SIF) Python Client**

> What is SIF?

The Singularity Image Format is a compressed [squashfs](https://en.wikipedia.org/wiki/SquashFS) 
filesystem that has a [block organizational structure](https://github.com/sylabs/sif/blob/master/pkg/sif/sif.go) to include metadata and content for the container definition file,
the header, partition, signatures (if present), and of course, the container
binary itself. 

> Why SIF Python?

One of the languages of scientific computing is Python. Singularity is implemented in GoLang.
Given the discrepancy, if your analysis pipeline is using Python, it's not currently 
easy to interact with metadata from the SIF binary from your environment.
Given that containers are a core ingredient of scientific reproducibility, 
we need to be able to read and understand them using Python.

SIF Python will allow you to interact with the container metadata included 
in SIF without needing GoLang. If you don't mind GoLang or sending commands 
to the terminal from within Python, then you
can use [SifTool](https://github.com/sylabs/sif/tree/master/cmd/siftool).

> Where do I go from here?

A good place to start is the [getting started]({{ site.baseurl }}/getting-started/) page.
