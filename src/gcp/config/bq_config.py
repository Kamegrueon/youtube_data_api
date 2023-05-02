from google.cloud import bigquery

MOST_POPULAR_TABLE_SCHEMA = [
    bigquery.SchemaField(
        'VIDEO_ID', 'STRING', mode='REQUIRED', description='動画ID'
    ),
    bigquery.SchemaField(
        'TITLE', 'STRING', mode='REQUIRED', description='動画のタイトル'
    ),
    bigquery.SchemaField(
        'CHANNEL_ID', 'STRING', mode='REQUIRED', description='チャンネルID'
    ),
    bigquery.SchemaField(
        'CHANNEL_TITLE', 'STRING', mode='REQUIRED', description='チャンネルのタイトル'
    ),
    bigquery.SchemaField(
        'PUBLISHED_AT', 'DATETIME', mode='REQUIRED', description='投稿日'
    ),
    bigquery.SchemaField(
        'CREATED_AT', 'DATETIME', mode='REQUIRED', description='データ取得日'
    ),
    bigquery.SchemaField(
        'CATEGORY_ID', 'STRING', mode='REQUIRED', description='カテゴリID'
    ),
    bigquery.SchemaField(
        'DURATION', 'STRING', mode='REQUIRED', description='動画の長さ'
    ),
    bigquery.SchemaField(
        'VIEW_COUNT', 'INTEGER', mode='NULLABLE', description='視聴回数'
    ),
    bigquery.SchemaField(
        'LIKE_COUNT', 'FLOAT', mode='NULLABLE', description='高評価数'
    ),
    bigquery.SchemaField(
        'DISLIKE_COUNT', 'FLOAT', mode='NULLABLE', description='低評価数'
    ),
    bigquery.SchemaField(
        'FAVORITE_COUNT', 'STRING', mode='NULLABLE', description='お気に入り数'
    ),
    bigquery.SchemaField(
        'COMMENT_COUNT', 'STRING', mode='NULLABLE', description='コメント数'
    ),
    bigquery.SchemaField(
        'TAGS', 'RECORD', mode='REPEATED', description='タグ情報',
        fields=[
            bigquery.SchemaField(
                'TAG_NAME', 'STRING', mode='NULLABLE', description='タグ名称'
            ),
        ])
]
