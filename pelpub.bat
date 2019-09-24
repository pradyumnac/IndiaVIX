call wenv\scripts\activate
pelican content -s publishconf.py -t themes\octopress
ghp-import output && git push github gh-pages
set /p message="Press any key to exit.."