echo 'Retrieving data to json local file'
rclone lsjson drive:Audiobooks -R > audiobooks.json
echo 'Processing data'
cat process.py | pbcopy
echo 'Running ipython with data copied'
pipenv run ipython
