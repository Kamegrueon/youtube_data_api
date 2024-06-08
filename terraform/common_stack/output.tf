output "app_service_account" {
  value = google_service_account.app
}

output "invoker_service_account" {
  value = google_service_account.invoker
}

output "artifact_registory" {
  value = module.artifact_registry
}
