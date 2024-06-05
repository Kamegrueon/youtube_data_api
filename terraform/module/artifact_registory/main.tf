resource "google_artifact_registry_repository" "repository" {
  description   = "Docker repository for ${var.app_name}"
  format        = "DOCKER"
  location      = var.gcp_region
  project       = var.gcp_project_id
  repository_id = "${var.app_name}-repository"

  cleanup_policy_dry_run = false
  cleanup_policies {
    id     = "delete-prerelease"
    action = "DELETE"
    condition {
      tag_state = "ANY"
    }
  }
  cleanup_policies {
    id     = "keep-minimum-versions"
    action = "KEEP"
    most_recent_versions {
      keep_count = 3
    }
  }
}
