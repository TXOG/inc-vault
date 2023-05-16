#!/bin/bash

# Get the current path using pwd
current_path=$(pwd)

# Build the alias line to be added to ~/.bashrc
alias_line="alias inc-vault='cd $current_path && python3 $current_path/IncVault.py'"

# Append the alias line to ~/.bashrc
echo "$alias_line" >> ~/.bashrc
