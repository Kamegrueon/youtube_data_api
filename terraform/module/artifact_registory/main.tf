resource "google_artifact_registry_repository" "repository" {
  description   = "Cloud Run repository for ${var.repository_name}"
  format        = "DOCKER"
  location      = var.gcp_region
  project       = var.gcp_project_id
  repository_id = "${var.repository_name}-repository"

  cleanup_policy_dry_run = false
  cleanup_policies {
    id     = "delete-prerelease"
    action = "DELETE"
    condition {
      tag_state = "ANY"
    }
  }
  dynamic "cleanup_policies" {
    # keep_countが0以下の場合は下記のcleanup_polycyを適用しない(dev環境はimageを保持しない)
    for_each = var.keep_count > 0 ? [var.keep_count] : []
    content {
      id     = "keep-minimum-versions"
      action = "KEEP"
      most_recent_versions {
        keep_count = cleanup_policies.value
      }
    }
  }
}
