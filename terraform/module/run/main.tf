# ローカル変数を使用して、コンテナのイメージを定義します。
# コンテナイメージは、指定されたvar.container_imageが空でない場合はそれを、そうでない場合はGoogle Artifact Registryからのイメージを使用します。
locals {
  image = var.container_image != "" ? var.container_image : "${var.repository_location}-docker.pkg.dev/${var.gcp_project_id}/${var.repository_name}/${terraform.workspace}-api-image:${var.docker_tag}"
}

# Cloud Run v2 サービスを定義します。このサービスはAPIとして公開され、内部専用のトラフィックを受け付けます。
resource "google_cloud_run_v2_service" "api" {
  name     = "${terraform.workspace}-${var.app_name}-api" # サービスの名前を指定します。
  location = var.gcp_region                               # サービスのデプロイ先のリージョンを指定します。
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"              # 内部からのトラフィックのみ受け付けるように設定します。

  # サービスのテンプレートを定義します。
  template {
    scaling {
      min_instance_count = 0 # サービスの最小インスタンス数を設定します。
      max_instance_count = 3 # サービスの最大インスタンス数を設定します。
    }

    service_account = var.service_account_app_email # サービスの実行に使用するサービスアカウントを指定します。

    containers {
      image = local.image # コンテナイメージを指定します。
      resources {
        limits = {
          cpu    = "1000m" # コンテナのCPUリソースの制限を設定します。
          memory = "1Gi"   # コンテナのメモリリソースの制限を設定します。
        }
        cpu_idle = true # コンテナがアイドル状態である場合にCPUリソースを解放するかどうかを設定します。
      }

      # サービスに渡す環境変数を指定します。
      env {
        name  = "GOOGLE_PROJECT_ID" # Google Cloud プロジェクトのIDを指定します。
        value = var.gcp_project_id  # Google Cloud プロジェクトのIDを設定します。
      }
      env {
        name  = "PUBSUB_GENERATE_ANNOTATIONS_TOPIC" # Pub/Subのトピック名を指定します。
        value = var.pubsub_topic_name               # Pub/Subのメイントピックの名前を設定します。
      }
      env {
        name  = "CLOUD_STORAGE_BUCKET"  # Cloud Storageバケット名を指定します。
        value = var.storage_bucket_name # Cloud Storageバケットの名前を設定します。
      }
      env {
        name  = "YOUTUBE_API_SERVICE_NAME"
        value = "youtube"
      }
      env {
        name  = "YOUTUBE_API_VERSION"
        value = "v3"
      }
      env {
        name  = "SECRET_ID"
        value = "YOUTUBE_API_KEY"
      }

      env {
        name  = "SECRET_YOUTUBE_API_VERSION"
        value = "1"
      }
    }
  }

  # サービスに対するトラフィックのターゲットを設定します。
  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST" # トラフィックのタイプを指定します。
    percent = 100                                     # サービスに対するトラフィックの割合を設定します。
  }
}

# APIを呼び出すためのIAMロールをサービスに付与します。
resource "google_cloud_run_service_iam_member" "api_invoker" {
  location = google_cloud_run_v2_service.api.location              # サービスのデプロイ先のリージョンを指定します。
  project  = google_cloud_run_v2_service.api.project               # サービスが所属するプロジェクトを指定します。
  service  = google_cloud_run_v2_service.api.name                  # サービスの名前を指定します。
  role     = "roles/run.invoker"                                   # サービスに付与するIAMロールを指定します。
  member   = "serviceAccount:${var.service_account_invoker_email}" # Invokerサービスアカウントにこのロールを付与します。
}
