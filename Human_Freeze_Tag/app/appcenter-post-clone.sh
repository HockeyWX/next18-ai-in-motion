#!/usr/bin/env bash
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo $APPCENTER_SOURCE_DIRECTORY
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

echo $FIREBASE_KEY | base64 -D  > $APPCENTER_SOURCE_DIRECTORY/Human_Freeze_Tag/app/google-services.json
cat $APPCENTER_SOURCE_DIRECTORY/Human_Freeze_Tag/app/google-services.json