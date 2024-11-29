#!/bin/bash

# Default commit message if none is provided
DEFAULT_MSG="Updated .docx files"

# Check if a commit message was provided
if [ -z "$1" ]; then
    echo "No commit message provided. Using default: \"$DEFAULT_MSG\""
    COMMIT_MSG="$DEFAULT_MSG"
else
    COMMIT_MSG="$1"
fi

# Stage untracked .docx files
echo "Staging untracked .docx files..."
git ls-files --others --exclude-standard -- "*.docx" | while IFS= read -r file; do
    git add "$file"
done

# Stage modified .docx files
echo "Staging modified .docx files..."
git ls-files --modified -- "*.docx" | while IFS= read -r file; do
    git add "$file"
done

# Stage deleted .docx files
echo "Staging deleted .docx files..."
git ls-files --deleted -- "*.docx" | while IFS= read -r file; do
    git rm "$file"
done

# Stage other tracked changes
echo "Staging tracked changes..."
git add -u

# Commit the changes
echo "Committing with message: \"$COMMIT_MSG\""
git commit -m "$COMMIT_MSG"

# Success message
echo "Commit completed successfully."
