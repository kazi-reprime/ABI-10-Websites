#!/usr/bin/env bash
# Push this repo to GitHub. Usage:
#   GITHUB_TOKEN=ghp_xxx GH_USER=yourname REPO=abi-ten ./push.sh
# Needs a token with 'repo' scope (classic) or a fine-grained token with repo read/write.
set -e
: "${GH_USER:?set GH_USER}"; : "${REPO:?set REPO}"; : "${GITHUB_TOKEN:?set GITHUB_TOKEN}"
# create the repo (ignore error if it already exists)
curl -s -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos -d "{\"name\":\"$REPO\",\"private\":false,\"description\":\"American Barber Institute — ten website concepts\"}" >/dev/null || true
git remote remove origin 2>/dev/null || true
git remote add origin "https://${GH_USER}:${GITHUB_TOKEN}@github.com/${GH_USER}/${REPO}.git"
git branch -M main
git push -u origin main
echo "Pushed → https://github.com/${GH_USER}/${REPO}  (enable Settings → Pages, branch main, / root)"
