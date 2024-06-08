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
