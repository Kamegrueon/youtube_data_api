variable "gcp_project_id" {
  type = string
}

variable "gcp_region" {
  type = string
}

variable "app_name" {
  type = string
}

variable "repository_location" {}
variable "repository_name" {}
variable "service_account_app_email" {}
variable "service_account_invoker_email" {}

variable "pubsub_topic_name" {}
variable "storage_bucket_name" {}

variable "container_image" {
  description = "Container image to deploy, must be in the same project as the app or public. If not specified, a default image will be used"
  type        = string
}

variable "docker_tag" {}
