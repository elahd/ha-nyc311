#!/usr/bin/env bash

container install
pip install --upgrade pip
pip install -r requirements-dev.txt
pre-commit install
pre-commit install-hooks
chmod +x /workspaces/ha-nyc311/.devcontainer/post-set-version-hook.sh

lib_dir="/workspaces/nyc311calendar"
repo_url="https://github.com/elahd/nyc311calendar.git"

if [ ! -d $lib_dir ]; then
    echo "Cloning nyc311calendar repository..."
    git clone "$repo_url" "$lib_dir"
else
    echo "nyc311calendar repository directory already exists."
fi

cd /workspaces/nyc311calendar
python setup.py develop
