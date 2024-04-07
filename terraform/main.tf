locals {
  terraformadmin_project_id = var.gcp_project_id
  terraform_service_account = "terraform@youtube-data-api-385206.iam.gserviceaccount.com"
}

terraform {
  required_version = ">= 1.4.2"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
  backend "gcs" {
    bucket                      = "youtube-data-api-terraform"
    prefix                      = "state/dev"
    impersonate_service_account = "terraform@youtube-data-api-385206.iam.gserviceaccount.com"
  }
}

provider "google" {
  project         = var.gcp_project_id
  region          = var.gcp_region
  access_token    = data.google_service_account_access_token.default.access_token
  request_timeout = "60s"
}

provider "google" {
  alias = "impersonation"
  scopes = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
  ]
}

data "google_service_account_access_token" "default" {
  provider               = google.impersonation
  target_service_account = local.terraform_service_account
  scopes                 = ["userinfo-email", "cloud-platform"]
  lifetime               = "1200s"
}


# https://registry.terraform.io/modules/terraform-google-modules/project-factory/google/14.0.0/submodules/project_services
module "enable_google_apis" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 14.0"

  project_id                  = var.gcp_project_id
  enable_apis                 = var.enable_apis
  disable_services_on_destroy = false
  disable_dependent_services  = false

  activate_apis = [
    "artifactregistry.googleapis.com",
    "bigquery.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "cloudscheduler.googleapis.com",
    "iamcredentials.googleapis.com",
    "iam.googleapis.com",
    "pubsub.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    "storage.googleapis.com",
    "youtube.googleapis.com"
  ]
}
