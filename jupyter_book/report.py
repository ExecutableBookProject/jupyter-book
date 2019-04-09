import os.path as op
import os
import sys
import shutil as sh
from ruamel.yaml import YAML
import nbformat as nbf
from subprocess import run, PIPE
from .utils import print_message_box
from distutils.dir_util import copy_tree
from glob import glob

def new_report(path_notebook, path_output, css, js, overwrite=False):
    """Create a new report from a single notebook."""

    name_notebook = op.basename(path_notebook)

    # Remove an old report if we want
    if op.isdir(path_output):
        if overwrite is True:
            sh.rmtree(path_output)
        else:
            raise ValueError(f"Found a pre-existing report at {path_output}. Please delete it or use `--overwrite`.")

    # Copy the notebook to a temporary folder
    print("Creating temporary folder...")
    path_temp = op.join(path_output, 'TMP')
    raw_folder = op.join(path_temp, 'raw')

    # Content we'll use to build the report
    path_config = op.join(raw_folder, '_config.yml')
    path_content = op.join(raw_folder, 'content')
    path_out = op.join(path_content, op.basename(path_notebook))

    # The temporary book goes here
    path_book = op.join(path_temp, 'book')

    # HTML for the built report
    path_html = op.join(path_temp, 'html')

    os.makedirs(path_content, exist_ok=True)
    sh.copy2(path_notebook, path_out)

    ## Hide code cells
    ntbk = nbf.read(path_out, nbf.NO_CONVERT)
    for cell in ntbk['cells']:
        if cell['cell_type'] == 'code':
            tags = cell['metadata'].get('tags', [])
            if not 'hidecode' in tags:
                tags.append('hidecode')
            cell['metadata']['tags'] = tags
    nbf.write(ntbk, path_out)


    ##### Create book for the report ###############################################

    # Add some config for a report
    yaml = YAML()
    config = {'show_sidebar': False, "baseurl": "", "url": ""}
    with open(path_config, 'w') as ff:
        yaml.dump(config, ff)

    # Create the new book
    print("Creating new book...")
    cmd = f"jupyter-book create {path_book} --content-folder {path_content} --config {path_config} --overwrite"
    out = run(cmd.split(), check=True)

    # Build the markdown for it
    print("Building book markdown...")
    cmd = f"jupyter-book build {path_book}"
    out = run(cmd.split(), check=True)

    # Build the HTML in the temp folder
    print("Building report HTML...")
    path_html_rel_build_folder = op.relpath(path_html, path_book)
    cmd = f'bundle exec jekyll build -d {path_html_rel_build_folder}'
    err = run(cmd.split(), check=True, cwd=path_book)

    ##### Clean up HTML ###########################################################

    # Move the content HTML file to the index.html spot
    path_html_index = op.join(path_html, "index.html")
    os.remove(path_html_index)
    sh.move(op.join(path_html, name_notebook.replace('.ipynb', '.html')), path_html_index)

    # Remove paths relative to root of folder
    with open(path_html_index, 'r') as ff:
        text = ff.read()
        text = text.replace('href="/', 'href="')
        text = text.replace('src="/', 'src="')
    with open(path_html_index, 'w') as ff:
        ff.write(text)

    # Copy into the output directory, overwriting it
    copy_tree(path_html, path_output)
    sh.rmtree(path_temp)
    path_output_index = op.join(path_output, 'index.html')
    msg = f"Done generating report!\n\nYour report is here: {path_output_index}"
    print_message_box(msg)