#!/bin/bash

# Fetch and pull the latest changes from the remote repository
echo "Updating from remote repository..."
git fetch origin
git pull origin main
