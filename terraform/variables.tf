##########################################
# Common
##########################################
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
# Cloud Run
##########################################

variable "container_image" {}
variable "docker_tag" {} # 実行時に引数として指定

##########################################
# IAM
##########################################

variable "app_roles" {}
