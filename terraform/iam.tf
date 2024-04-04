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
