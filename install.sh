#!/bin/bash

sudo apt install python3-nautilus
mkdir -p ~/.local/share/nautilus-python/extensions/
cp nautilus-tracker-extension.py ~/.local/share/nautilus-python/extensions/
nautilus -q