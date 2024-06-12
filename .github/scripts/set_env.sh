#!/bin/bash

if [[ "$GITHUB_REF" == "refs/heads/main" || "$GITHUB_BASE_REF" == "main" ]]; then
  echo "ENV_STRING=prd" >> "$GITHUB_OUTPUT"
elif [[ "$GITHUB_REF" == "refs/heads/stg" || "$GITHUB_BASE_REF" == "stg" ]]; then
  echo "ENV_STRING=stg" >> "$GITHUB_OUTPUT"
fi