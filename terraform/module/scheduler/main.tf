locals {
  invoke_params = {
    store = {
      prefix = "most_popular"
      part   = "id"
      filter = {
        chart = "mostPopular"
      }
      maxResults = 50
    }
  }

  messages = [
    {
      url_path = "/invoke"
      action   = "store"
      params   = local.invoke_params.store
    }
  ]
}

resource "google_cloud_scheduler_job" "invoke_transfer" {
  for_each    = { for i in local.messages : i.url_path => i }
  paused      = terraform.workspace == "prd" ? false : true
  name        = "${terraform.workspace}-invoke-transfer"
  project     = var.gcp_project_id
  schedule    = "0 12 * * *"
  description = "Invoke Cloud Run Transfer Job on Schedule"
  time_zone   = "Asia/Tokyo"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = "${var.cloud_run_api_uri}${each.value.url_path}"

    body = base64encode(jsonencode({
      action = each.value.action
      params = each.value.params
    }))

    headers = {
      "Content-Type" = "application/json"
    }

    oidc_token {
      service_account_email = var.service_account_invoker_email
      audience              = "${var.cloud_run_api_uri}${each.value.url_path}"
    }
  }
}
