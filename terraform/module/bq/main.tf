resource "google_bigquery_dataset" "dataset" {
  dataset_id  = "${terraform.workspace}-videos"
  location    = "US"
  description = "YouTube Data API Dataset"
}
