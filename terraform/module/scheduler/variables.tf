variable "gcp_project_id" {
  type = string
}

variable "gcp_region" {
  type = string
}

variable "app_name" {
  type = string
}

variable "invoke_transfer_url_path" {
  type    = string
  default = "/invoke/transfer"
}

variable "cloud_run_api_uri" {}
variable "service_account_invoker_email" {}