# Jupyter Book for developers

## API reference from docstrings

If you are using Jupyter Book for package documentation,
it can be time-saving to use [the sphinx autodoc extension](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
to automatically generate the API reference documentation.
To do so,
you first need to add the `autodoc` extension to `_config.yaml`:

```yaml
sphinx:
  extra_extensions:
  - 'sphinx.ext.autodoc'
```

Then,
you can either use the [MyST eval_rst directive](https://myst-parser.readthedocs.io/en/latest/using/howto.html?highlight=rst#use-sphinx-ext-autodoc-in-markdown-files),
or create a separate .rst file for the API reference page.
This file can be called anything (e.g. `api.rst`)
as long as it is referenced in `_toc.yml`,
and it should look something like this:

```rst
API Reference
=============

.. automodule:: my_project.my_module
    :members:
```

The next time you build your book,
`autodoc` will extract all the docstrings from that module
and create a single documentation page for all of them.
If you want more control and the table of contents in the right margin,
you can add headings and functions individually:

```rst
API Reference
=============

Func one
--------
.. autofunction:: my_project.my_module.func_one

Func two
--------
.. autofunction:: my_project.my_module.func_two
```

If your docstrings are written per the NumPy or Google conventions,
you can add [the napoleon extension](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#module-sphinx.ext.napoleon) to parse and render them correctly.
Another useful extension
can insert a link to the source code for each function
and there is an option to shorten the function names to just the basename:

```
sphinx:
  extra_extensions:
  - 'sphinx.ext.autodoc'
  - 'sphinx.ext.napoleon'
  - 'sphinx.ext.viewcode'
  config:
    add_module_names: False
```

If you have a more complex project structure
and want to recursively extract docstrings of all submodules and their functions,
you can use [the autosummary extension](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html)
with the `:recursive:` option (since Sphinx 3.1).

```
sphinx:
  extra_extensions:
  - 'sphinx.ext.autodoc'
  - 'sphinx.ext.autosummary'
  config:
    autosummary_generate: True
```

Your `api.rst` file should now look like this:

```rst

API documentation
=================

.. autosummary::
   :toctree: _autosummary
   :recursive:

   my_module
```

To insert clickable links from the summary page
to each functions docstring,
you are currently [required to modify the default templates](https://stackoverflow.com/a/62613202/2166823),
and [links will not be enabled by default until at least Sphinx 4](https://github.com/sphinx-doc/sphinx/issues/7912).
Another option to generate clickable links to functions recursively
is the [autoapi extension](https://sphinx-autoapi.readthedocs.io/en/latest/tutorials.html#setting-up-automatic-api-documentation-generation),
which can be installed via pip
and requires less customization than the above.
