resource "google_bigquery_dataset" "dataset" {
  dataset_id  = "${terraform.workspace}_videos"
  location    = "US"
  description = "YouTube Data API Dataset"
}

resource "google_bigquery_table" "most_popular" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "${terraform.workspace}_most_popular"
  time_partitioning {
    type  = "DAY"
    field = "CREATED_AT"
  }

  clustering = ["CHANNEL_ID", "CATEGORY_ID"]

  schema = <<EOF
[
  {
    "name": "VIDEO_ID",
    "mode": "REQUIRED",
    "type": "STRING",
    "description": "動画ID",
    "fields": []
  },
  {
    "name": "TITLE",
    "mode": "REQUIRED",
    "type": "STRING",
    "description": "動画のタイトル",
    "fields": []
  },
  {
    "name": "CHANNEL_ID",
    "mode": "REQUIRED",
    "type": "STRING",
    "description": "チャンネルID",
    "fields": []
  },
  {
    "name": "CHANNEL_TITLE",
    "mode": "REQUIRED",
    "type": "STRING",
    "description": "チャンネルのタイトル",
    "fields": []
  },
  {
    "name": "PUBLISHED_AT",
    "mode": "REQUIRED",
    "type": "DATETIME",
    "description": "投稿日",
    "fields": []
  },
  {
    "name": "CREATED_AT",
    "mode": "REQUIRED",
    "type": "DATETIME",
    "description": "データ取得日",
    "fields": []
  },
  {
    "name": "CATEGORY_ID",
    "mode": "REQUIRED",
    "type": "INTEGER",
    "description": "カテゴリID",
    "fields": []
  },
  {
    "name": "DURATION",
    "mode": "REQUIRED",
    "type": "STRING",
    "description": "動画の長さ",
    "fields": []
  },
  {
    "name": "VIEW_COUNT",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": "視聴回数",
    "fields": []
  },
  {
    "name": "LIKE_COUNT",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": "高評価数",
    "fields": []
  },
  {
    "name": "DISLIKE_COUNT",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": "低評価数",
    "fields": []
  },
  {
    "name": "FAVORITE_COUNT",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": "お気に入り数",
    "fields": []
  },
  {
    "name": "COMMENT_COUNT",
    "mode": "NULLABLE",
    "type": "INTEGER",
    "description": "コメント数",
    "fields": []
  },
  {
    "name": "TAGS",
    "mode": "REPEATED",
    "type": "STRING",
    "description": "タグ情報",
    "fields": []
  }
]
EOF
}



resource "google_bigquery_dataset_iam_member" "bigquery_editor_role" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${var.service_account_app_email}" # メンバーを指定します。
}
