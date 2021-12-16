echo 'Retrieving data to json local file'
rclone lsjson drive:Audiobooks -R > audiobooks.json
echo 'Processing data'
cat process.py | pbcopy
echo 'Running ipyhon with data copied'
pipenv run ipython
