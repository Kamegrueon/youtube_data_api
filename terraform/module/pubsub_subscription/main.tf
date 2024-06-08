# メッセージのサブスクリプションを定義します。
# サブスクリプション名は、アプリケーションの名前に"-sub"が追加されたものになります。
resource "google_pubsub_subscription" "main" {
  name  = "${terraform.workspace}-${var.app_name}-sub" # サブスクリプションの名前は、アプリケーション名に"-sub"が追加されたものになります。
  topic = var.pubsub_topic_id                          # このサブスクリプションが購読するトピックを指定します。

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
    dead_letter_topic     = var.pubsub_topic_dead_letter_id # デッドレタートピックを指定します。
    max_delivery_attempts = 5                               # メッセージの最大配信試行回数を設定します。
  }

  # Pushの設定を行います。
  push_config {
    push_endpoint = "${var.cloud_run_uri}${var.main_subscription_url_path}" # Pushのエンドポイントを設定します。
    oidc_token {
      service_account_email = var.service_account_invoker_email # OIDCトークンのサービスアカウントのメールアドレスを指定します。
    }
    attributes = {
      x-goog-version = "v1" # 属性を指定します。
    }
  }
}

# サブスクリプションにサブスクライバーのロールを割り当てます。
resource "google_pubsub_subscription_iam_member" "subscription_subscriber_role" {
  subscription = google_pubsub_subscription.main.name              # ロールを割り当てるサブスクリプションを指定します。
  role         = "roles/pubsub.subscriber"                         # サブスクライバーのロールを指定します。
  member       = "serviceAccount:${var.service_account_app_email}" # メンバーを指定します。
}
