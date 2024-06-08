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
  source          = "../module/artifact_registory"
  for_each        = { for config in var.artifact_registry_configs : config.name => config }
  gcp_project_id  = var.gcp_project_id
  gcp_region      = var.gcp_region
  repository_name = "${each.value.name}-${var.app_name}"
  keep_count      = each.value.keep_count
  depends_on      = [module.enable_google_apis]
}
