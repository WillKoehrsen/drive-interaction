echo 'Retrieving data to json local file'
rclone lsjson drive:IFTTT/reddit -R > drive_photos.json
echo 'Processing data'
cat process.py | pbcopy