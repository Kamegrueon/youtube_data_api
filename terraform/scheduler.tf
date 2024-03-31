resource "google_cloud_scheduler_job" "invoke-transfer" {
  name        = "invoke-transfer"
  project     = var.gcp_project_id
  schedule    = "0 12 * * *"
  description = "suggesting your lunch"
  time_zone   = "Asia/Tokyo"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_v2_service.api.uri}${var.invoke_transfer_url_path}"

    oidc_token {
      service_account_email = google_service_account.invoker.email
    }
  }

  depends_on = [module.enable_google_apis]

}
