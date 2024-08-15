locals {
  files       = fileset("${path.module}/../static_tables", "*/*.yaml")
  directories = distinct([for path in local.files : dirname(path)])
}

resource "google_bigquery_dataset" "dataset" {
  for_each    = toset(local.directories)
  dataset_id  = "${terraform.workspace}_${each.key}"
  location    = "US"
  description = "YouTube Data API Dataset"
}

resource "google_bigquery_dataset_iam_member" "bigquery_editor_role" {
  for_each = google_bigquery_dataset.dataset

  dataset_id = each.value.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${var.service_account_app_email}"
}
