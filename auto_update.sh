#!/bin/bash
# ==============================================================================
# Auto-Update Script: Push changes to GitHub Pages instantly
# ==============================================================================

set -e

MSG="${1:-Update Hubban-ul-Lughat dictionary}"

git add .gitignore 1782975618016.png index.html words.js data.js tailwind.js manifest.json sw.js urdu_bangla.json Prompt.txt sync_all.py generate_20k_dictionary.py verified_words.json auto_update.sh verified_alif.json verified_alif_madd.json build_and_deploy_alif_1000.py build_and_deploy_alif_2400.py
git commit -m "$MSG" || echo "No changes to commit"
git push origin main

echo "===================================================="
echo " LIVE UPDATE DEPLOYED TO GITHUB PAGES!"
echo " URL: https://ahmadhibban.github.io/hubban-ul-lughat/"
echo "===================================================="
