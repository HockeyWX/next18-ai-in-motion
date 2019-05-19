#!/usr/bin/env bash
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo $APPCENTER_SOURCE_DIRECTORY
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

echo $FIREBASE_KEY | base64 -D  > $APPCENTER_SOURCE_DIRECTORY/app/google-services.json