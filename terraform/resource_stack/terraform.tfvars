##########################################
# Common
##########################################
terraform_sa_admin_email  = "terraform@youtube-data-api-385206.iam.gserviceaccount.com"
terraform_sa_viewer_email = "terraform-viewer@youtube-data-api-385206.iam.gserviceaccount.com"

gcp_project_id = "youtube-data-api-385206"
gcp_region     = "asia-northeast1"
app_name       = "youtube-data-api"

enable_apis = true
activate_apis = [
  "artifactregistry.googleapis.com",
  "bigquery.googleapis.com",
  "cloudresourcemanager.googleapis.com", # Resource Manager
  "cloudscheduler.googleapis.com",
  "iamcredentials.googleapis.com", # Service Account Credentials
  "iam.googleapis.com",
  "sts.googleapis.com", # Security Token Service API
  "pubsub.googleapis.com",
  "run.googleapis.com",
  "secretmanager.googleapis.com",
  "storage.googleapis.com",
  "youtube.googleapis.com"
]


container_image = ""

app_roles = [
  "roles/bigquery.jobUser",
  "roles/bigquery.dataEditor",
  "roles/run.serviceAgent",
  "roles/pubsub.publisher",
  "roles/storage.objectCreator",
  "roles/secretmanager.secretAccessor"
]
