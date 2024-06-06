locals {
  terraform_service_account = "terraform@youtube-data-api-385206.iam.gserviceaccount.com"
  github_repo_owner         = "Kamegrueon"
  github_repository         = "youtube_data_api"
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
    prefix = "state"
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
  target_service_account = local.terraform_service_account
  scopes                 = ["userinfo-email", "cloud-platform"]
  lifetime               = "300s"
}

provider "google" {
  project         = var.gcp_project_id
  region          = var.gcp_region
  access_token    = data.google_service_account_access_token.default.access_token
  request_timeout = "60s"
}

# Workload Identity Pool 設定
resource "google_iam_workload_identity_pool" "youtube_data_api_pool" {
  project                   = var.gcp_project_id
  workload_identity_pool_id = "youtube-data-api-pool"
  display_name              = "youtube-data-api-pool"
  description               = "GitHub Actions で使用"
}

# Workload Identity Provider 設定
resource "google_iam_workload_identity_pool_provider" "youtube_data_api_provider" {
  project                            = var.gcp_project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.youtube_data_api_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "youtube-data-api-provider"
  display_name                       = "youtube-data-api-provider"
  description                        = "GitHub Actions で使用"
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
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.youtube_data_api_pool.name}/attribute.repository/${local.github_repo_owner}/${local.github_repository}"
  role               = "roles/iam.workloadIdentityUser"
}

# https://registry.terraform.io/modules/terraform-google-modules/project-factory/google/14.0.0/submodules/project_services
# APIの有効化モジュール
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

module "artifact_registry" {
  source         = "./module/artifact_registory"
  gcp_project_id = var.gcp_project_id
  gcp_region     = var.gcp_region
  app_name       = var.app_name
  depends_on     = [module.enable_google_apis]
}

module "pubsub_topic" {
  source                    = "./module/pubsub_topic"
  gcp_project_id            = var.gcp_project_id
  gcp_region                = var.gcp_region
  app_name                  = var.app_name
  service_account_app_email = google_service_account.app.email
  depends_on                = [module.enable_google_apis]
}

module "pubsub_subscription" {
  source                        = "./module/pubsub_subscription"
  gcp_project_id                = var.gcp_project_id
  gcp_region                    = var.gcp_region
  app_name                      = var.app_name
  cloud_run_uri                 = module.run.cloud_run_api_uri
  pubsub_topic_id               = module.pubsub_topic.pubsub_topic_id
  pubsub_topic_dead_letter_id   = module.pubsub_topic.pubsub_topic_dead_letter_id
  service_account_invoker_email = google_service_account.invoker.email
  service_account_app_email     = google_service_account.app.email
  depends_on                    = [module.enable_google_apis, module.run]
}

module "scheduler" {
  source                        = "./module/scheduler"
  gcp_project_id                = var.gcp_project_id
  gcp_region                    = var.gcp_region
  app_name                      = var.app_name
  cloud_run_api_uri             = module.run.cloud_run_api_uri
  service_account_invoker_email = google_service_account.invoker.email
  depends_on                    = [module.enable_google_apis]
}

module "storage" {
  source                    = "./module/storage"
  gcp_project_id            = var.gcp_project_id
  gcp_region                = var.gcp_region
  app_name                  = var.app_name
  service_account_app_email = google_service_account.app.email
  depends_on                = [module.enable_google_apis]
}

module "run" {
  source                        = "./module/run"
  gcp_project_id                = var.gcp_project_id
  gcp_region                    = var.gcp_region
  app_name                      = var.app_name
  service_account_app_email     = google_service_account.app.email
  service_account_invoker_email = google_service_account.invoker.email
  repository_location           = module.artifact_registry.repository_location
  repository_name               = module.artifact_registry.repository_name
  container_image               = var.container_image
  docker_tag                    = var.docker_tag
  storage_bucket_name           = module.storage.storage_bucket_name
  pubsub_topic_name             = module.pubsub_topic.pubsub_topic_name
  depends_on                    = [module.enable_google_apis, module.pubsub_topic, module.storage]
}
