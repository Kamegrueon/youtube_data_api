#!/bin/bash

lf="\n"  # GitHub Actionsの改行エスケープシーケンス

# メッセージの構築
message="#### Terraform Format and Style 🖌${FMT_OUTCOME}${lf}"
message+="#### Terraform Initialization ⚙️${INIT_OUTCOME}${lf}"
message+="#### Terraform Validation 🤖${VALIDATE_OUTCOME}${lf}"
message+="<details><summary>Validation Output</summary>${lf}"
message+="\`\`\`${lf}${lf}"
message+="${VALIDATE_OUTPUT}${lf}"
message+="\`\`\`${lf}"
message+="</details>${lf}"
message+="#### Terraform Plan 📖${PLAN_OUTCOME}${lf}"
message+="<details><summary>Show Plan</summary>${lf}"
message+="\`\`\`terraform${lf}${lf}"
message+="${PLAN_OUTPUT}${lf}"
message+="\`\`\`${lf}"
message+="</details>${lf}"
message+="* Pusher: @${GITHUB_ACTOR}, Action: ${GITHUB_EVENT_NAME}, Working Directory: ${GITHUB_WORKING_DIR}, Workflow: ${GITHUB_WORKFLOW} *"

# メッセージの出力
echo -e $message > terraform_comment.txt