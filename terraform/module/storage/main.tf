resource "google_storage_bucket" "bucket" {
  name          = "${terraform.workspace}-${var.gcp_project_id}-bucket"
  location      = var.gcp_region
  force_destroy = terraform.workspace == "prd" ? false : true
}

resource "google_storage_bucket_iam_member" "member" {
  bucket = google_storage_bucket.bucket.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${var.service_account_app_email}"
}
