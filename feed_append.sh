#!/bin/bash

python feed_append.py $1

# echo "Downloading $FEED_FILE and $SHUFFLED_FEED_FILE."
# sftp $SFTP_USER@$SFTP_HOST <<EOF
# 	get $REMOTE_DIR/$FEED_FILE $FEED_FILE
# 	get $REMOTE_DIR/$SHUFFLED_FEED_FILE $SHUFFLED_FEED_FILE
# EOF

# echo
# echo "Uploading $FEED_FILE and $SHUFFLED_FEED_FILE."
# sftp $SFTP_USER@$SFTP_HOST <<EOF
# 	put $FEED_FILE $REMOTE_DIR/$FEED_FILE
# 	put $SHUFFLED_FEED_FILE $REMOTE_DIR/$SHUFFLED_FEED_FILE
# EOF

exit 0
