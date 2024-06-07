# https://registry.terraform.io/modules/terraform-google-modules/project-factory/google/14.0.0/submodules/project_services
# APIの有効化モジュール
module "enable_google_apis" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 14.0"

  project_id                  = var.gcp_project_id
  enable_apis                 = var.enable_apis
  disable_services_on_destroy = false
  disable_dependent_services  = false
  activate_apis               = var.activate_apis
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
