#!/bin/bash

lf=$'\n'
message="#### Terraform Format and Style 🖌${FMT_OUTCOME}"
message+="${lf}#### Terraform Initialization ⚙️${INIT_OUTCOME}"
message+="${lf}#### Terraform Validation 🤖${VALIDATE_OUTCOME}"
message+="${lf}<details><summary>Validation Output</summary>"
message+="${lf}\`\`\`"
message+="${lf}${VALIDATE_OUTPUT}"
message+="${lf}\`\`\`"
message+="${lf}</details>"
message+="${lf}#### Terraform Plan 📖${PLAN_OUTCOME}"
message+="${lf}<details><summary>Show Plan</summary>"
message+="${lf}\`\`\`"
message+="${lf}terraform\n${PLAN_OUTPUT}"
message+="${lf}\`\`\`"
message+="${lf}</details>"
message+="${lf}*Pusher: @${GITHUB_ACTOR}, Action: ${GITHUB_EVENT_NAME}, Working Directory: ${GITHUB_WORKING_DIR}, Workflow: ${GITHUB_WORKFLOW}*"
echo "message=${message}" >> $GITHUB_OUTPUT