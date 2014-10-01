Goal
====

The goal of this project is to provide an online tool to help creating new
slide decks from slides of existing ones.

**Note that this is a very young baby that still needs love before walking.**

Setting up
==========

First thing is to install virtualenv and pip python tools to avoid changing too
heavily the system python packages. On an openSUSE box, you can you:

    zypper in python-virtualenv python pip

Then create and use the python virtual environment (let's say in the `./data`
folder):

    virtualenv ./data
    . ./data/bin/activate

From now install the python dependencies:

    pip install CherryPy
    pip install lpod-python
    pip install bottle
    pip install lxml

Copy and modify the `local.json.example` file into `local.json` and then
run the `slideapi.py` script.
