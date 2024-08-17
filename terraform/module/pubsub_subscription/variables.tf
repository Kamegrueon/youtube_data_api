variable "gcp_project_id" {
  type = string
}

variable "gcp_region" {
  type = string
}

variable "app_name" {
  type = string
}

variable "cloud_run_uri" {}

variable "service_account_invoker_email" {}
variable "service_account_app_email" {}
variable "pubsub_topic_id" {}
variable "pubsub_topic_dead_letter_id" {}

variable "main_subscription_url_path" {
  type    = string
  default = "/invoke"
}

variable "invoke_transfer_url_path" {
  type    = string
  default = "/invoke/transfer"
}
