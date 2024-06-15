#!/bin/bash

lf="%0A"  # GitHub Actionsの改行エスケープシーケンス

# メッセージの構築
message="#### Terraform Format and Style 🖌${FMT_OUTCOME}${lf}"
message+="#### Terraform Initialization ⚙️${INIT_OUTCOME}${lf}"
message+="#### Terraform Validation 🤖${VALIDATE_OUTCOME}${lf}"
message+="<details><summary>Validation Output</summary>${lf}\`\`\`${lf}${VALIDATE_OUTPUT}${lf}\`\`\`${lf}</details>${lf}"
message+="#### Terraform Plan 📖${PLAN_OUTCOME}${lf}"
message+="<details><summary>Show Plan</summary>${lf}\`\`\`terraform${lf}${PLAN_OUTPUT}${lf}\`\`\`${lf}</details>${lf}"
message+="*Pusher: @${GITHUB_ACTOR}, Action: ${GITHUB_EVENT_NAME}, Working Directory: ${GITHUB_WORKING_DIR}, Workflow: ${GITHUB_WORKFLOW}*"

# メッセージの出力
echo "message=$message" >> $GITHUB_OUTPUT