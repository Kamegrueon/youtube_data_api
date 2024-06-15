##########################################
# Common
##########################################
variable "run_context" {
  type = string
}

variable "terraform_sa_admin_email" {
  type = string
}

variable "terraform_sa_viewer_email" {
  type = string
}

variable "github_repo_owner" {
  type = string
}

variable "github_repository" {
  type = string
}

variable "gcp_project_id" {
  type = string
}

variable "gcp_region" {
  type = string
}

variable "app_name" {
  type = string
}

variable "enable_apis" {
  type = bool
}

variable "activate_apis" {}

##########################################
# IAM
##########################################

variable "terraform_role" {}
variable "app_roles" {}
variable "invoker_role" {}

##########################################
# Artifact Registory
##########################################
variable "artifact_registry_configs" {
  type = list(object({
    name       = string
    keep_count = number
  }))
}
