locals {
  terraformadmin_project_id = var.gcp_project_id
  terraform_service_account = "terraform@youtube-data-api-385206.iam.gserviceaccount.com"
  github_repo_owner         = "Kamegrueon"
  github_repository         = "youtube_data_api"
  #   project_id        = "myproject"
  #   region            = "asia-northeast1"

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
    bucket = "youtube-data-api-terraform"
    prefix = "state/dev"
    # impersonate_service_account = "terraform@youtube-data-api-385206.iam.gserviceaccount.com"
  }
}

provider "google" {
  project         = var.gcp_project_id
  region          = var.gcp_region
  access_token    = data.google_service_account_access_token.default.access_token
  request_timeout = "60s"
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
  target_service_account = local.terraform_service_account
  scopes                 = ["userinfo-email", "cloud-platform"]
  lifetime               = "300s"
}

# Workload Identity Pool 設定
resource "google_iam_workload_identity_pool" "mypool" {
  #   provider                  = google-beta
  project                   = local.terraformadmin_project_id
  workload_identity_pool_id = "mypool"
  display_name              = "mypool"
  description               = "GitHub Actions で使用"
}

# Workload Identity Provider 設定
resource "google_iam_workload_identity_pool_provider" "myprovider" {
  #   provider                           = google-beta
  project                            = local.terraformadmin_project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.mypool.workload_identity_pool_id
  workload_identity_pool_provider_id = "myprovider"
  display_name                       = "myprovider"
  description                        = "GitHub Actions で使用"
  #   attribute_condition                = "assertion.repository_owner == \"${local.github_repo_owner}\""
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.actor"      = "assertion.actor"
  }

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

data "google_service_account" "terraform_sa" {
  account_id = local.terraform_service_account
}

resource "google_service_account_iam_member" "terraform_sa" {
  service_account_id = data.google_service_account.terraform_sa.id
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.mypool.name}/attribute.repository/${local.github_repo_owner}/${local.github_repository}"
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
    "cloudresourcemanager.googleapis.com", # Resource Manager
    "cloudscheduler.googleapis.com",
    "iamcredentials.googleapis.com", # Service Account Credentials
    "iam.googleapis.com",
    "sts.googleapis.com", # Security Token Service API
    "pubsub.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    "storage.googleapis.com",
    "youtube.googleapis.com"
  ]
}
