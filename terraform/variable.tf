variable "prefix" {
  type    = string
  default = "dev"
}

variable "gcp_project_name" {
  type    = string
  default = "youtube-data-api"
}

variable "gcp_project_id" {
  type = string
}

variable "gcp_region" {
  type = string
}

variable "enable_apis" {
  type    = bool
  default = true
}

##########################################
# Application
##########################################
variable "app_name" {
  type    = string
  default = "youtube-data-api"
}

variable "main_subscription_url_path" {
  type    = string
  default = "/invoke/load"
}

variable "invoke_transfer_url_path" {
  type    = string
  default = "/invoke/transfer"
}

##########################################
# Cloud Run
##########################################

variable "container_image" {}

variable "docker_tag" {}

##########################################
# IAM
##########################################

variable "app_roles" {
  default = [
    "roles/bigquery.jobUser",
    "roles/bigquery.dataEditor",
    "roles/run.serviceAgent",
    "roles/pubsub.publisher",
    "roles/storage.objectCreator",
    "roles/secretmanager.secretAccessor"
  ]

}
