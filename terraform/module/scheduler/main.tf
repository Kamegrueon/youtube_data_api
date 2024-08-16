locals {
  params = [
    {
      url_path : "/invoke/transfer",
      prefix : "most_popular",
      part : "snippet, contentDetails, statistics",
      chart : "mostPopular",
      maxResults : 50
    }
  ]
}

resource "google_cloud_scheduler_job" "invoke-transfer" {
  for_each    = { for i in local.params : i.url_path => i }
  paused      = terraform.workspace == "prd" ? false : true
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
    uri         = "${var.cloud_run_api_uri}${each.value.url_path}"
    body        = base64encode("{\"prefix\":\"${each.value.prefix}\",\"part\":\"${each.value.part}\",\"chart\":\"${each.value.chart}\",\"maxResults\":${each.value.maxResults}}")
    headers = {
      "Content-Type" = "application/json"
    }

    oidc_token {
      service_account_email = var.service_account_invoker_email
      audience              = "${var.cloud_run_api_uri}${each.value.url_path}"
    }
  }

}
