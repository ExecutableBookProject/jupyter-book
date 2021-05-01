"""A small sphinx extension to let you configure a site with YAML metadata."""
from os.path import relpath, isdir
from pathlib import Path
from functools import lru_cache
import json
from typing import Collection, Optional, Union, Set
from glob import glob
import jsonschema
import yaml
import sys
import os
from nested_lookup import nested_lookup
from .utils import _message_box

# Transform a "Jupyter Book" YAML configuration file into a Sphinx configuration file.
# This is so that we can choose more user-friendly words for things than Sphinx uses.
# e.g., 'logo' instead of 'html_logo'.
# Note that this should only be used for **top level** keys.
PATH_YAML_DEFAULT = Path(__file__).parent.joinpath("default_config.yml")
PATH_JSON_SCHEMA = Path(__file__).parent.joinpath("config_schema.json")


def get_default_sphinx_config():
    """Some configuration values that are really sphinx-specific."""
    return dict(
        extensions=[
            "sphinx_togglebutton",
            "sphinx_copybutton",
            "myst_nb",
            "jupyter_book",
            "sphinx_thebe",
            "sphinx_comments",
            "sphinx.ext.intersphinx",
            "sphinx_panels",
            "sphinx_book_theme",
        ],
        language=None,
        pygments_style="sphinx",
        html_theme="sphinx_book_theme",
        html_theme_options={"search_bar_text": "Search this book..."},
        html_add_permalinks="¶",
        html_sourcelink_suffix="",
        numfig=True,
        panels_add_bootstrap_css=False,
        suppress_warnings=["myst.domains"],
    )


@lru_cache(1)
def get_validator():
    schema = json.loads(PATH_JSON_SCHEMA.read_text("utf8"))
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    return validator_cls(schema=schema)


def validate_yaml(yaml: dict, raise_on_errors=False, print_func=print):
    """Validate the YAML configuration against a JSON schema."""
    errors = sorted(get_validator().iter_errors(yaml), key=lambda e: e.path)
    error_msg = "\n".join(
        [
            "- {} [key path: '{}']".format(
                error.message, "/".join([str(p) for p in error.path])
            )
            for error in errors
        ]
    )
    if not errors:
        return
    if raise_on_errors:
        raise jsonschema.ValidationError(error_msg)
    return _message_box(
        f"Warning: Validation errors in config:\n{error_msg}",
        color="orange",
        print_func=print_func,
    )


def get_final_config(
    toc: Optional[Path],
    user_yaml: Optional[Union[dict, Path]] = None,
    cli_config: Optional[dict] = None,
    sourcedir: Optional[Path] = None,
    validate: bool = True,
    raise_on_invalid: bool = False,
):
    """Create the final configuration dictionary, to parser to sphinx

    :param user_config_path: A path to a YAML file written by the user
    :param cli_config: Configuration coming directly from the CLI
    :param sourcedir: path to source directory.
        If it contains a `_static` folder, we ad that to the final `html_static_path`
    :param validate: Validate user yaml against the data schema
    :param raise_on_invalid: Raise a ValidationError, or only log a warning

    Order of precedence is:

    1. CLI Sphinx Configuration
    2. User JB(YAML) Configuration
    3. Default JB (YAML) Configuration
    4. Default Sphinx Configuration

    """

    # get the default sphinx configuration
    sphinx_config = get_default_sphinx_config()

    # get the default yaml configuration
    yaml_config, default_yaml_update, add_paths = yaml_to_sphinx(
        yaml.safe_load(PATH_YAML_DEFAULT.read_text(encoding="utf8"))
    )
    yaml_config.update(default_yaml_update)

    # if available, get the user defined configuration
    user_yaml_recurse, user_yaml_update = {}, {}
    user_yaml_path = None
    if user_yaml:
        if isinstance(user_yaml, Path):
            user_yaml_path = user_yaml
            user_yaml = yaml.safe_load(user_yaml.read_text(encoding="utf8"))
        else:
            user_yaml = user_yaml
        if validate:
            validate_yaml(user_yaml, raise_on_errors=raise_on_invalid)

        if user_yaml.get("only_build_toc_files"):
            if not toc:
                raise ValueError("you must have a toc to use `only_build_toc_files`")
            excluded_patterns = set(user_yaml.get("exclude_patterns", []))

            newly_excluded = _get_files_outside_toc(toc, sourcedir, excluded_patterns)
            user_yaml["exclude_patterns"] = sorted(
                excluded_patterns.union(newly_excluded)
            )

        user_yaml_recurse, user_yaml_update, add_paths = yaml_to_sphinx(user_yaml)

    # add paths from yaml config
    if user_yaml_path:
        for path in add_paths:
            path = (user_yaml_path.parent / path).resolve()
            sys.path.append(path.as_posix())

    # first merge the user yaml into the default yaml
    _recursive_update(yaml_config, user_yaml_recurse)

    # then merge this into the default sphinx config
    _recursive_update(sphinx_config, yaml_config)

    # Value set in `sphinx: config: ...` are a special case,
    # and completely override any defaults (sphinx and yaml)
    sphinx_config.update(user_yaml_update)

    # This is to deal with a special case, where the override needs to be applied after
    # the sphinx app is initialised (since the default is a function)
    # TODO I'm not sure if there is a better way to deal with this?
    config_meta = {
        "latex_doc_overrides": sphinx_config.pop("latex_doc_overrides"),
        "latex_individualpages": cli_config.pop("latex_individualpages"),
    }

    if sphinx_config.get("use_multitoc_numbering"):
        sphinx_config["extensions"].append("sphinx_multitoc_numbering")

    if sphinx_config.get("use_jupyterbook_latex"):
        sphinx_config["extensions"].append("jupyterbook_latex")

    # finally merge in CLI configuration
    _recursive_update(sphinx_config, cli_config or {})

    # Add the `_static` folder to html_static_path, only if it exists
    if sourcedir and Path(sourcedir).joinpath("_static").is_dir():
        paths_static = sphinx_config.get("html_static_path", [])
        paths_static.append("_static")
        sphinx_config["html_static_path"] = paths_static

    return sphinx_config, config_meta


def yaml_to_sphinx(yaml: dict):
    """Convert a Jupyter Book style config structure into a Sphinx config dict.

    :returns: (recursive_updates, override_updates, add_paths)

    add_paths collects paths that are specified in the _config.yml (such as those
    provided in local_extensions) and returns them for adding to sys.path in
    a context where the _config.yml path is known
    """
    sphinx_config = {}

    # top-level, string type
    YAML_TRANSLATIONS = {
        "title": "html_title",
        "author": "author",
        "copyright": "copyright",
        "logo": "html_logo",
        "project": "project",
        "use_multitoc_numbering": "use_multitoc_numbering",
    }
    for key, newkey in YAML_TRANSLATIONS.items():
        if key in yaml:
            val = yaml.get(key)
            if val is None:
                val = ""
            sphinx_config[newkey] = val

    # exclude patterns
    if "exclude_patterns" in yaml:
        # we always include these excludes, so as not to break back-compatibility
        defaults = {"_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"}
        defaults.update(yaml["exclude_patterns"])
        sphinx_config["exclude_patterns"] = list(sorted(defaults))

    # Theme
    sphinx_config["html_theme_options"] = theme_options = {}
    if "launch_buttons" in yaml:
        theme_options["launch_buttons"] = yaml["launch_buttons"]

    repository_config = yaml.get("repository", {})
    for spx_key, yml_key in [
        ("path_to_docs", "path_to_book"),
        ("repository_url", "url"),
        ("repository_branch", "branch"),
    ]:
        if yml_key in repository_config:
            theme_options[spx_key] = repository_config[yml_key]

    # HTML
    html = yaml.get("html")
    if html:

        for spx_key, yml_key in [
            ("html_favicon", "favicon"),
            ("html_baseurl", "baseurl"),
            ("comments_config", "comments"),
        ]:
            if yml_key in html:
                sphinx_config[spx_key] = html[yml_key]

        for spx_key, yml_key in [
            ("google_analytics_id", "google_analytics_id"),
            ("navbar_footer_text", "navbar_footer_text"),
            ("extra_navbar", "extra_navbar"),
            # Deprecate navbar_footer_text after a release cycle
            ("extra_footer", "extra_footer"),
            ("home_page_in_toc", "home_page_in_navbar"),
        ]:
            if yml_key in html:
                theme_options[spx_key] = html[yml_key]

        # Pass through the buttons
        btns = ["use_repository_button", "use_edit_page_button", "use_issues_button"]
        use_buttons = {btn: html.get(btn) for btn in btns if btn in html}
        if any(use_buttons.values()):
            if not repository_config.get("url"):
                raise ValueError(
                    "To use 'repository' buttons, you must specify the repository URL"
                )
        # Update our config
        theme_options.update(use_buttons)

    # Parse and Rendering
    parse = yaml.get("parse")
    if parse:
        # Enable extra extensions
        extensions = sphinx_config.get("myst_enable_extensions", [])
        # TODO: deprecate this in v0.11.0
        if parse.get("myst_extended_syntax") is True:
            extensions.append(
                [
                    "colon_fence",
                    "dollarmath",
                    "amsmath",
                    "deflist",
                    "html_image",
                ]
            )
            _message_box(
                (
                    "myst_extended_syntax is deprecated, instead specify extensions "
                    "you wish to be enabled. See https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html"  # noqa: E501
                ),
                color="orange",
                print_func=print,
            )
        for ext in parse.get("myst_enable_extensions", []):
            if ext not in extensions:
                extensions.append(ext)
        if extensions:
            sphinx_config["myst_enable_extensions"] = extensions

        # Configuration values we'll just pass-through
        for ikey in ["myst_substitutions", "myst_url_schemes"]:
            if ikey in parse:
                sphinx_config[ikey] = parse.get(ikey)

    # Execution
    execute = yaml.get("execute")
    if execute:
        for spx_key, yml_key in [
            ("execution_allow_errors", "allow_errors"),
            ("execution_in_temp", "run_in_temp"),
            ("nb_output_stderr", "stderr_output"),
            ("execution_timeout", "timeout"),
            ("jupyter_cache", "cache"),
            ("jupyter_execute_notebooks", "execute_notebooks"),
            ("execution_excludepatterns", "exclude_patterns"),
        ]:
            if yml_key in execute:
                sphinx_config[spx_key] = execute[yml_key]

        if sphinx_config.get("jupyter_execute_notebooks") is False:
            # Special case because YAML treats `off` as "False".
            sphinx_config["jupyter_execute_notebooks"] = "off"

    # LaTeX
    latex = yaml.get("latex")
    if latex:
        for spx_key, yml_key in [
            ("latex_engine", "latex_engine"),
            ("use_jupyterbook_latex", "use_jupyterbook_latex"),
        ]:
            if yml_key in latex:
                sphinx_config[spx_key] = latex[yml_key]

    sphinx_config["latex_doc_overrides"] = {}
    if "title" in yaml:
        sphinx_config["latex_doc_overrides"]["title"] = yaml["title"]
    for key, val in yaml.get("latex", {}).get("latex_documents", {}).items():
        sphinx_config["latex_doc_overrides"][key] = val

    # Sphinx Configuration
    extra_extensions = yaml.get("sphinx", {}).get("extra_extensions")
    if extra_extensions:
        sphinx_config["extensions"] = get_default_sphinx_config()["extensions"]

        if not isinstance(extra_extensions, list):
            extra_extensions = [extra_extensions]

        for extension in extra_extensions:
            if extension not in sphinx_config["extensions"]:
                sphinx_config["extensions"].append(extension)

    local_extensions = yaml.get("sphinx", {}).get("local_extensions")
    # add_paths collects additional paths for sys.path
    add_paths = []
    if local_extensions:
        if "extensions" not in sphinx_config:
            sphinx_config["extensions"] = get_default_sphinx_config()["extensions"]
        for extension, path in local_extensions.items():
            if extension not in sphinx_config["extensions"]:
                sphinx_config["extensions"].append(extension)
            if path not in sys.path:
                add_paths.append(path)

    # Citations
    sphinxcontrib_bibtex_configs = ["bibtex_bibfiles", "bibtex_reference_style"]
    if any(ii in yaml for ii in sphinxcontrib_bibtex_configs):
        # Load sphincontrib-bibtex
        if "extensions" not in sphinx_config:
            sphinx_config["extensions"] = get_default_sphinx_config()["extensions"]
        sphinx_config["extensions"].append("sphinxcontrib.bibtex")

        # Pass through configuration
        if yaml.get("bibtex_bibfiles"):
            if isinstance(yaml.get("bibtex_bibfiles"), str):
                yaml["bibtex_bibfiles"] = [yaml["bibtex_bibfiles"]]
            sphinx_config["bibtex_bibfiles"] = yaml["bibtex_bibfiles"]

    # items in sphinx.config will override defaults,
    # rather than recursively updating them
    return sphinx_config, yaml.get("sphinx", {}).get("config") or {}, add_paths


def _recursive_update(config, update, list_extend=False):
    """Update the dict `config` with `update` recursively.
    This *updates* nested dicts / lists instead of replacing them.
    """
    for key, val in update.items():
        if isinstance(config.get(key), dict):
            # if a dict value update is set to None,
            # then the entire dict will be "wiped",
            # otherwise it is recursively updated.
            if isinstance(val, dict):
                _recursive_update(config[key], val, list_extend)
            else:
                config[key] = val
        elif isinstance(config.get(key), list):
            if isinstance(val, list) and list_extend:
                config[key].extend(val)
            else:
                config[key] = val
        else:
            config[key] = val


def _get_files_outside_toc(
    toc: Path, sourcedir: Path, excluded_patterns: Collection[str]
) -> Set[str]:
    """Returns a set of files that are outside of the toc for exclusion from sphinx.

    Hidden files are NOT processed here as it may result in thousands of individual
     exclusions.
    """
    source_root = sourcedir or Path()
    source_files = {ff for ff in glob(str(source_root / "**/*"), recursive=True)}

    excluded_file_sets = [set(glob(pp, recursive=True)) for pp in excluded_patterns]
    included_files: Set[str] = {
        Path(relpath(ff, source_root)).as_posix()
        for ff in source_files.difference(*excluded_file_sets)
        if not isdir(ff)
    }

    toc_yaml = yaml.safe_load(toc.read_text(encoding="utf8"))
    toc_files = {ff for ff in nested_lookup("file", toc_yaml)}

    verified_toc_files: Set[str] = {
        Path(ff).as_posix()
        for ff in included_files
        if os.path.splitext(ff)[0] in toc_files or ff in toc_files
    }
    return included_files.difference(verified_toc_files)
