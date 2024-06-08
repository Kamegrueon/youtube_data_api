##########################################
# Common
##########################################
terraform_sa_email = "terraform@youtube-data-api-385206.iam.gserviceaccount.com"
github_repo_owner  = "Kamegrueon"
github_repository  = "youtube_data_api"
gcp_project_id     = "youtube-data-api-385206"
gcp_region         = "asia-northeast1"
app_name           = "youtube-data-api"

enable_apis = true
activate_apis = [
  "iamcredentials.googleapis.com", # Service Account Credentials
  "iam.googleapis.com",
  "sts.googleapis.com", # Security Token Service API
]

terraform_role = "roles/iam.workloadIdentityUser"

app_roles = [
  "roles/bigquery.jobUser",
  "roles/bigquery.dataEditor",
  "roles/run.serviceAgent",
  "roles/pubsub.publisher",
  "roles/storage.objectCreator",
  "roles/secretmanager.secretAccessor"
]

invoker_role = "roles/run.invoker"

artifact_registry_configs = [
  {
    name       = "prd"
    keep_count = 3
  },
  {
    name       = "dev"
    keep_count = 0
  }
]

