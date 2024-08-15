locals {
  files       = fileset("${path.module}/../static_tables", "*/*.yaml")
  directories = distinct([for path in local.files : dirname(path)])
}

resource "google_bigquery_table" "tables" {
  for_each   = local.files
  dataset_id = "${terraform.workspace}_${split("/", each.value)[0]}"

  table_id = "${terraform.workspace}_${trimsuffix(split("/", each.value)[1], ".yaml")}"
  schema   = jsonencode(yamldecode(file("${path.module}/../static_tables/${each.value}"))["schema"])

  # パーティショニング設定
  time_partitioning {
    type  = yamldecode(file("${path.module}/../static_tables/${each.value}"))["partitioning"]["type"]
    field = yamldecode(file("${path.module}/../static_tables/${each.value}"))["partitioning"]["field"]
  }

  clustering = yamldecode(file("${path.module}/../static_tables/${each.value}"))["clustering"]["fields"]

  deletion_protection = terraform.workspace == "prd" ? true : false

  lifecycle {
    ignore_changes = [
      schema,
      time_partitioning,
      clustering,
    ]
  }
}
