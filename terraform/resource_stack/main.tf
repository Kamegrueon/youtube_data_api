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


module "pubsub_topic" {
  source                    = "../module/pubsub_topic"
  gcp_project_id            = var.gcp_project_id
  gcp_region                = var.gcp_region
  app_name                  = var.app_name
  service_account_app_email = data.terraform_remote_state.common.outputs.app_service_account.email
  depends_on                = [module.enable_google_apis]
}

module "pubsub_subscription" {
  source                        = "../module/pubsub_subscription"
  gcp_project_id                = var.gcp_project_id
  gcp_region                    = var.gcp_region
  app_name                      = var.app_name
  cloud_run_uri                 = module.run.cloud_run_api_uri
  pubsub_topic_id               = module.pubsub_topic.pubsub_topic_id
  pubsub_topic_dead_letter_id   = module.pubsub_topic.pubsub_topic_dead_letter_id
  service_account_invoker_email = data.terraform_remote_state.common.outputs.invoker_service_account.email
  service_account_app_email     = data.terraform_remote_state.common.outputs.app_service_account.email
  depends_on                    = [module.enable_google_apis, module.run]
}

module "scheduler" {
  source                        = "../module/scheduler"
  gcp_project_id                = var.gcp_project_id
  gcp_region                    = var.gcp_region
  app_name                      = var.app_name
  cloud_run_api_uri             = module.run.cloud_run_api_uri
  service_account_invoker_email = data.terraform_remote_state.common.outputs.invoker_service_account.email
  depends_on                    = [module.enable_google_apis]
}

module "storage" {
  source                    = "../module/storage"
  gcp_project_id            = var.gcp_project_id
  gcp_region                = var.gcp_region
  app_name                  = var.app_name
  service_account_app_email = data.terraform_remote_state.common.outputs.app_service_account.email
  depends_on                = [module.enable_google_apis]
}

module "bq_datasets" {
  source                    = "../module/bq/bq_datasets"
  service_account_app_email = data.terraform_remote_state.common.outputs.app_service_account.email
  depends_on                = [module.enable_google_apis]
}

module "bq_tables" {
  source     = "../module/bq/bq_tables"
  depends_on = [module.enable_google_apis, module.bq_datasets]
}

module "run" {
  source                        = "../module/run"
  gcp_project_id                = var.gcp_project_id
  gcp_region                    = var.gcp_region
  app_name                      = var.app_name
  service_account_app_email     = data.terraform_remote_state.common.outputs.app_service_account.email
  service_account_invoker_email = data.terraform_remote_state.common.outputs.invoker_service_account.email
  repository_location           = data.terraform_remote_state.common.outputs.artifact_registory[terraform.workspace].repository.location
  repository_name               = data.terraform_remote_state.common.outputs.artifact_registory[terraform.workspace].repository.name
  container_image               = var.container_image
  docker_tag                    = var.docker_tag
  storage_bucket_name           = module.storage.storage_bucket_name
  pubsub_topic_name             = module.pubsub_topic.pubsub_topic_name
  environment                   = terraform.workspace
  depends_on                    = [module.enable_google_apis, module.pubsub_topic, module.storage]
}
