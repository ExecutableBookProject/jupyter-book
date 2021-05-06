# Structure of your table of contents

Your book's structure is determined by a **Table of Contents**.
This is a YAML file (called `_toc.yml`) that defines a structure that Jupyter Book uses to create the order and nesting of pages.

:::{admonition} Building articles or single pages
:class: seealso
You can also build an **article** (or a single page) rather than an entire book.
This works similarly to the instructions detailed below.
See [](../basics/page.md) for more information.
:::

:::{admonition} Migrate to the new Table of Contents structure
:class: warning
A new Table of Contents structure was introduced in `v0.11`.
To migrate your old TOC structure to the new structure, use the following command:

```shell
jupyter-book toc migrate path/to/_toc.yml -o path/to/_toc.yml
```

This will overwrite your `_toc.yml` file with the new version.
:::

## Basic Table of Contents structure

The table of contents is broadly organized like so:

```yaml
format: jb-book
root: index
chapters:
- file: path/to/chapter1
- file: path/to/chapter2
```

Here is a brief explanation of each key:

`format:`
: Defines the structure of this Table of Contents (e.g., how to interpret the key names). `jb-book` tells Jupyter Book to expect `chapters` and `parts` terminology (see below for details).

`root:`
: The first page of your book (aka, the "root page").
  It is the landing page for the HTML of your book.

`chapters:`
: A list of entries, each of which maps onto **chapters** of your book.

## Types of chapter/section entries

There are several types of entries that you may provide in order to point to specific types of content.
Here is a quick overview:

`file:`
: A path that points to a local text file, which defines the content of this entry (the chapter, section, or sub-section).
  These paths should be relative to your `_toc.yml` file.

`glob:`
: A [glob-like pattern](https://docs.python.org/3/library/glob.html) that can be used to match against **multiple local files**.
  Each of these files will be collected and inserted into your content, in the order that `glob` discovers them.

`url:`
: An external link to a website (starting with `http` or `https`).
  This will be inserted into your book's Table of Contents, though it will not affect your book's structure (like numbering).

## Use chapter sub-sections

You may optionally split a chapter across multiple files (each making up a **section** of the chapter).
To do so, use the `sections:` configuration, like so:

```yaml
format: jb-book
root: index
chapters:
- file: path/to/chapter1
- file: path/to/chapter2
  sections:
  - file: path/to/chapter2/section1
```

Here's a brief explanation of `sections:`

`sections:`
: A list of entries that define **sub-sections** of a chapter.
  This is useful if you'd like to split a chapter across multiple pages.
  See [](toc/structure) for more information.

## Use parts to organize chapters

You may optionally organize your chapters into **parts**, by using the `parts:` key like so:

```yaml
format: jb-book
root: index
parts:
  - caption: Name of Part 1
    chapters:
    - file: path/to/part1/chapter1
    - file: path/to/part1/chapter2
      sections:
      - file: path/to/part1/chapter2/section1
  - caption: Name of Part 2
    chapters:
    - file: path/to/part2/chapter1
    - file: path/to/part2/chapter2
      sections:
      - file: path/to/part2/chapter2/section1
```

Here's a brief explanation of `parts:`

`parts:`
: A list of entries, each of which defines a chapter.
  This is useful if you'd like to use different groups of chapters.

(toc/configuration-structure)=
## Configuration structure

In addition to structuring your book, you may also use your Table of Contents to control the behavior of your book via configuration.
This section covers the general structure that you should use to configure your book.

:::{seealso}
For information about the kinds of configuration at your disposal, see [](structure/configure)
:::

### Book-wide configuration

To configure options for your entire book, use the `defaults:` configuration at the root of your Table of Contents.
This configuration will be applied to every list of chapters and sections within your book.

For example:

```yaml
format: jb-book
root: index
defaults:  # The defaults key will be applied to all chapters and sub-sections
  numbered: True
chapters:
- file: path/to/chapter1
- file: path/to/chapter2
```

### Configuring one set of chapters

If you're only using a single list of chapters, and not organizing them into parts, you can configure these chapters with the `options:` key.

For example:

```yaml
format: jb-book
root: index
options:  # The options key will be applied to all chapters, but not sub-sections
  numbered: True
chapters:
- file: path/to/part1/chapter1
- file: path/to/part1/chapter2
```

### Configuring multiple parts

If you are organizing your book into **parts** (groups of chapters), you can configure each set of chapters separately by providing `key: value` pairs alongside each `part` entry, like so:

```yaml
format: jb-book
root: index
parts:
  - caption: Name of Numbered Part 1
    numbered: True  # Only applies to chapters in Part 1.
    chapters:
    - file: path/to/part1/chapter1
    - file: path/to/part1/chapter2
  - caption: Name of Not-numbered Part 2
    chapters:
    - file: path/to/part2/chapter1
    - file: path/to/part2/chapter2
```

In this case, the `numbered:` option would *only apply to Part 1*, and not Part 2.
