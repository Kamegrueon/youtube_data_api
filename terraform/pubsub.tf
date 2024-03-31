# Google Cloud Platform (GCP) のPub/Subトピックを定義します。
# このトピックは、アプリケーションの名前に基づいています。
resource "google_pubsub_topic" "main" {
  name = var.app_name # トピックの名前は、var.app_nameに指定されたアプリケーション名に設定されます。

  # このトピックの作成は、指定したモジュールが有効になった後に行われます。
  depends_on = [module.enable_google_apis]
}

# デッドレタートピックを定義します。メインのトピックの名前に"-dlq"が追加されたものになります。
resource "google_pubsub_topic" "main_dead_letter" {
  name = "${google_pubsub_topic.main.name}-dlq" # デッドレタートピックの名前は、メインのトピック名に"-dlq"が追加されたものになります。

  # このトピックの作成は、指定したモジュールが有効になった後に行われます。
  depends_on = [module.enable_google_apis]
}

# メッセージのサブスクリプションを定義します。
# サブスクリプション名は、アプリケーションの名前に"-sub"が追加されたものになります。
resource "google_pubsub_subscription" "main" {
  name  = "${var.app_name}-sub"         # サブスクリプションの名前は、アプリケーション名に"-sub"が追加されたものになります。
  topic = google_pubsub_topic.main.name # このサブスクリプションが購読するトピックを指定します。

  # メッセージのアックを待つ時間を設定します。
  ack_deadline_seconds = 599

  # メッセージの保持期間を設定します。
  message_retention_duration = "1200s" # メッセージの保持期間は、20分（1200秒）に設定されています。

  # メッセージの期限切れポリシーを設定します。
  expiration_policy {
    ttl = "" # メッセージの期限切れポリシーは設定されていません。
  }

  # リトライポリシーを設定します。
  retry_policy {
    minimum_backoff = "10s" # リトライの最小バックオフ時間を設定します。
  }

  # メッセージの順序付けを有効にするかどうかを指定します。
  enable_message_ordering = false

  # デッドレターポリシーを設定します。
  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.main_dead_letter.id # デッドレタートピックを指定します。
    max_delivery_attempts = 5                                       # メッセージの最大配信試行回数を設定します。
  }

  # Pushの設定を行います。
  push_config {
    push_endpoint = "${google_cloud_run_v2_service.api.uri}${var.main_subscription_url_path}" # Pushのエンドポイントを設定します。
    oidc_token {
      service_account_email = google_service_account.invoker.email # OIDCトークンのサービスアカウントのメールアドレスを指定します。
    }
    attributes = {
      x-goog-version = "v1" # 属性を指定します。
    }
  }
}

# サブスクリプションにサブスクライバーのロールを割り当てます。
resource "google_pubsub_subscription_iam_member" "subscription_subscriber_role" {
  subscription = google_pubsub_subscription.main.name                 # ロールを割り当てるサブスクリプションを指定します。
  role         = "roles/pubsub.subscriber"                            # サブスクライバーのロールを指定します。
  member       = "serviceAccount:${google_service_account.app.email}" # メンバーを指定します。
}

# トピックにパブリッシャーのロールを割り当てます。
resource "google_pubsub_topic_iam_member" "topic_publisher_role" {
  topic  = google_pubsub_topic.main.name                        # ロールを割り当てるトピックを指定します。
  role   = "roles/pubsub.publisher"                             # パブリッシャーのロールを指定します。
  member = "serviceAccount:${google_service_account.app.email}" # メンバーを指定します。
}
