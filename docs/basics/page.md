(publish:page)=
# Build an article

You can build an **article** (e.g., a single page) rather than an entire book.
You can build outputs for an article from a single source file, or split it up across multiple files (similar to how you'd structure a book).

This section contains more information about how to do this.

:::{admonition} Work in progress
Article building functionality for Jupyter Book is still under design and development.
This functionality may change over time!
If you have ideas, suggestions, or would like to help out, please [see the contributing guide](../contribute/intro.md).
:::

## Build an article from a single file

You can generate a standalone HTML file for a single page of the Jupyter Book using the `jupyter-book` command, and pointing it to a **single file** instead of a book's directory:

```bash
jupyter-book build path/to/mypage.ipynb
```

This will build the file as usual, and place it in an output folder called `_build/_page/html/<mypage>`.

If the file is in a subdirectory relative to the `_build` folder, the HTML will be in a `_build/_page/html/<subdirectory-mypage>` folder.

Your page will be called `mypage.html`.
This will work for any [content source file](../file-types/index.md) that is supported by Jupyter Book.


## Build an article from multiple files

You may also split an article across multiple input files (e.g., if you'd like to store sections separately).
To do so, use the `format: jb-article` option in your `_toc.yml` file.

For example:

```yaml
format: jb-article
root: index
sections:
- file: path/to/chapter1
- file: path/to/chapter2
```

The primary difference is that the `jb-book` format uses `parts:` and `chapters:` syntax, while the `jb-article` format uses `sections:` syntax alone.

The rest of the build process behaves similarly to how you'd build a book.
See [](build.md) for more details.
