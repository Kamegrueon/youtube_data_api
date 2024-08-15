locals {
  files       = fileset("${path.module}/static_tables", "*/*.yaml")
  directories = distinct([for path in local.files : dirname(path)])
}

resource "google_bigquery_dataset" "dataset" {
  for_each    = toset(local.directories)
  dataset_id  = "${terraform.workspace}_${each.key}"
  location    = "US"
  description = "YouTube Data API Dataset"
}

resource "google_bigquery_table" "tables" {
  for_each   = local.files
  dataset_id = "${terraform.workspace}_${split("/", each.value)[0]}"

  table_id = "${terraform.workspace}_${trimsuffix(split("/", each.value)[1], ".yaml")}"
  schema   = jsonencode(yamldecode(file("${path.module}/static_tables/${each.value}"))["schema"])

  # パーティショニング設定
  time_partitioning {
    type  = yamldecode(file("${path.module}/static_tables/${each.value}"))["partitioning"]["type"]
    field = yamldecode(file("${path.module}/static_tables/${each.value}"))["partitioning"]["field"]
  }

  clustering = yamldecode(file("${path.module}/static_tables/${each.value}"))["clustering"]["fields"]

  deletion_protection = terraform.workspace == "prd" ? true : false

  lifecycle {
    ignore_changes = [
      schema,
      time_partitioning,
      clustering,
    ]
  }
}


resource "google_bigquery_dataset_iam_member" "bigquery_editor_role" {
  for_each = google_bigquery_dataset.dataset

  dataset_id = each.value.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${var.service_account_app_email}"
}
