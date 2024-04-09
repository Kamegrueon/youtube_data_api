variable "prefix" {
  type    = string
  default = "dev"
}

variable "gcp_project_name" {
  type    = string
  default = "youtube-data-api"
}

variable "gcp_project_id" {
  type    = string
  default = "youtube-data-api-385206"
}

variable "gcp_region" {
  type    = string
  default = "asia-northeast1"
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

variable "container_image" {
  description = "Container image to deploy, must be in the same project as the app or public. If not specified, a default image will be used"
  type        = string
  default     = ""
}

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
