resource "google_cloud_scheduler_job" "invoke-transfer" {
  name        = "${terraform.workspace}-invoke-transfer"
  project     = var.gcp_project_id
  schedule    = "0 12 * * *"
  description = "suggesting your lunch"
  time_zone   = "Asia/Tokyo"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = "${var.cloud_run_api_uri}${var.invoke_transfer_url_path}"

    oidc_token {
      service_account_email = var.service_account_invoker_email
      audience              = "${var.cloud_run_api_uri}${var.invoke_transfer_url_path}"
    }
  }

}
