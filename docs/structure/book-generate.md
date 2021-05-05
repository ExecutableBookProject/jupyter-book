---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.10.3
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Generate book files from a Table of Contents

It is possible to use a `_toc.yml` file in order to create the skeleton of a book automatically.
This is useful if you wish to quickly generate empty files from a single structure, and then populate them with content yourselves.

To create your book's files from the Table of Contents, use the following command:

```bash
jupyter-book toc to-site path/to/_toc.yml
```

This will generate a collection of files according to the structure in `_toc.yml`.

In addition, you have a few options to control the behavior of this tool.
See below for reference.

```{code-cell}
:tags: [remove-input]
!jupyter-book toc to-site -h
```
