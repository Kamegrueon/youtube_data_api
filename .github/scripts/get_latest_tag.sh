#!/bin/bash

LATEST_TAG=$(gcloud artifacts docker images list --sort-by=~CREATE_TIME --include-tags --format='value(TAGS)' --filter="tags:*" --limit=1 "${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/${ENV_STRING}-api-image" || echo "default")
if [ "$LATEST_TAG" == "default" ]; then
  echo "Failed to get the latest tag, Use the tag default."
else
  echo "Latest image tag is $LATEST_TAG"
fi
echo "tag=$LATEST_TAG" >> "$GITHUB_OUTPUT"