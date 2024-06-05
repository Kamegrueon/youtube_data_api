variable "gcp_project_id" {
  type = string
}

variable "gcp_region" {
  type = string
}

variable "app_name" {
  type = string
}

variable "service_account_app_email" {}

variable "main_subscription_url_path" {
  type    = string
  default = "/invoke/load"
}

variable "invoke_transfer_url_path" {
  type    = string
  default = "/invoke/transfer"
}
