#!/bin/bash
# ==============================================================================
# Auto-Update Script: Push changes to GitHub Pages instantly
# ==============================================================================

set -e

MSG="${1:-Update Hubban-ul-Lughat dictionary}"

git add -A
git commit -m "$MSG" || echo "No changes to commit"
git push origin main

echo "===================================================="
echo " LIVE UPDATE DEPLOYED TO GITHUB PAGES!"
echo " URL: https://ahmadhibban.github.io/hubban-ul-lughat/"
echo "===================================================="
