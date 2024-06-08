locals {
  terraform_service_account = "terraform@youtube-data-api-385206.iam.gserviceaccount.com"
  github_repo_owner         = "Kamegrueon"
  github_repository         = "youtube_data_api"
}

data "google_service_account" "terraform_sa" {
  account_id = local.terraform_service_account
}

resource "google_service_account_iam_member" "terraform_sa" {
  service_account_id = data.google_service_account.terraform_sa.id
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.youtube_data_api_pool.name}/attribute.repository/${local.github_repo_owner}/${local.github_repository}"
  role               = "roles/iam.workloadIdentityUser"
}

resource "google_service_account" "app" {
  # account id can not be longer than 28 characters
  account_id   = substr("${var.app_name}-sa", 0, 28)
  display_name = "Service Account for ${var.app_name}"
}

resource "google_project_iam_member" "app" {
  project = var.gcp_project_id
  count   = length(var.app_roles)
  role    = element(var.app_roles, count.index)
  member  = "serviceAccount:${google_service_account.app.email}"
}

resource "google_service_account" "invoker" {
  account_id   = "cloudrun-invoker"
  display_name = "Cloud Run Invoker"
}

resource "google_project_iam_member" "invoker" {
  project = var.gcp_project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.invoker.email}"
}
