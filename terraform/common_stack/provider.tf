locals {
  terraform_sa_email = var.run_context == "remote" ? var.terraform_sa_admin_email : var.terraform_sa_viewer_email
}

terraform {
  required_version = ">= 1.4.2"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.28.0"
    }
  }
  backend "gcs" {
    bucket = "youtube-data-api-terraform"
    prefix = "state/common"
  }
}

# 有効期限の短いトークンを取得するためのプロバイダ
provider "google" {
  alias = "impersonation"
  scopes = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
  ]
}

# 有効期限の短いトークンを取得するためのデータ
data "google_service_account_access_token" "default" {
  provider               = google.impersonation
  target_service_account = local.terraform_sa_email
  scopes                 = ["userinfo-email", "cloud-platform"]
  lifetime               = "300s"
}

provider "google" {
  project         = var.gcp_project_id
  region          = var.gcp_region
  access_token    = data.google_service_account_access_token.default.access_token
  request_timeout = "60s"
}
