"""Build a book with Jupyter Notebooks and Sphinx."""
from pathlib import Path

from docutils import nodes

from .toc import add_toc_to_sphinx, add_toctree
from .directive.toc import TableofContents, SwapTableOfContents, TableOfContentsNode
from sphinx.util import logging


__version__ = "0.10.2"

logger = logging.getLogger(__name__)


def add_static_files(app, config):
    """Search the static files paths and initialize any CSS of JS files."""
    static_paths = config.html_static_path
    for path in static_paths:
        path = Path(app.confdir).joinpath(path)
        for path_css in path.rglob("*.css"):
            app.add_css_file((path_css.relative_to(path)).as_posix())
        for path_js in path.rglob("*.js"):
            app.add_js_file((path_js.relative_to(path)).as_posix())


def skip(self, node) -> None:
    raise nodes.SkipNode


# We connect this function to the step after the builder is initialized
def setup(app):

    # Updates `master_doc` using the first item of `_toc.yml`
    app.connect("config-inited", add_toc_to_sphinx)

    # Add toctrees to each content page using `_toc.yml`
    app.connect("source-read", add_toctree)

    # Path for `_toc.yml`
    app.add_config_value("globaltoc_path", "toc.yml", "env")
    app.add_config_value("use_jupyterbook_latex", True, "env")

    # Add custom static files to the sphinx build
    app.connect("config-inited", add_static_files)

    # Directives
    app.add_node(
        TableOfContentsNode,
        override=True,
        html=(skip, None),
        latex=(skip, None),
        textinfo=(skip, None),
        text=(skip, None),
        man=(skip, None),
    )
    app.add_directive("tableofcontents", TableofContents)

    # Transforms
    app.add_post_transform(SwapTableOfContents)

    # Extensions
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
