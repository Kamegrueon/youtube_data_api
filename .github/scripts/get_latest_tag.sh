#!/bin/bash

LATEST_TAG=$(gcloud artifacts docker images list --sort-by=~CREATE_TIME --include-tags --format='value(TAGS)' --filter="tags:*" --limit=1 "$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$ENV_STRING-api-image" || echo "default")
if [ "$LATEST_TAG" == "default" ]; then
  echo "Failed to get the latest tag. Setting tag name to 'default'."
elif [ "$LATEST_TAG" == "" ]; then
    LATEST_TAG="default"
    echo "No image found in Artifact Registry. Setting tag name to 'default'.”
else
  echo "Latest image tag is $LATEST_TAG"
fi
echo "tag=$LATEST_TAG" >> "$GITHUB_OUTPUT"