#!/bin/bash
# ==============================================================================
# Auto-Update Script: Push changes to GitHub Pages instantly
# ==============================================================================

set -e

MSG="${1:-Update Hubban-ul-Lughat dictionary}"

git add .gitignore 1782975618016.png index.html words.js data.js tailwind.js manifest.json sw.js urdu_bangla.json Prompt.txt verified_words.json auto_update.sh verified_alif.json verified_alif_madd.json letters/ LEXICON_PRINCIPLES.md Answer.txt
git commit -m "$MSG" || echo "No changes to commit"
git push origin main

echo "===================================================="
echo " LIVE UPDATE DEPLOYED TO GITHUB PAGES!"
echo " URL: https://ahmadhibban.github.io/hubban-ul-lughat/"
echo "===================================================="
