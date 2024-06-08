# Google Cloud Platform (GCP) のPub/Subトピックを定義します。
# このトピックは、アプリケーションの名前に基づいています。
resource "google_pubsub_topic" "main" {
  name = "${terraform.workspace}-${var.app_name}" # トピックの名前は、var.app_nameに指定されたアプリケーション名に設定されます。
}

# デッドレタートピックを定義します。メインのトピックの名前に"-dlq"が追加されたものになります。
resource "google_pubsub_topic" "main_dead_letter" {
  name = "${terraform.workspace}-${google_pubsub_topic.main.name}-dlq" # デッドレタートピックの名前は、メインのトピック名に"-dlq"が追加されたものになります。
}

# トピックにパブリッシャーのロールを割り当てます。
resource "google_pubsub_topic_iam_member" "topic_publisher_role" {
  topic  = google_pubsub_topic.main.name                     # ロールを割り当てるトピックを指定します。
  role   = "roles/pubsub.publisher"                          # パブリッシャーのロールを指定します。
  member = "serviceAccount:${var.service_account_app_email}" # メンバーを指定します。
}
