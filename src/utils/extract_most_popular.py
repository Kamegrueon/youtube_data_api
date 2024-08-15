# -*- coding: utf-8 -*-

def extract_datetime_from_file_path(file_path: str) -> str:
    split_str = file_path.split("/")[1]
    date = f"{split_str[0:4]}-{split_str[4:6]}-{split_str[6:8]}"
    time = f"{split_str[8:10]}:{split_str[10:12]}:00"
    return f"{date} {time}"


def extract_published(published_at: str) -> str:
    date = published_at[0:10]
    time = published_at[11:16]
    return f"{date} {time}:00"


def extract_most_popular(data: dict, created_at: str) -> list[dict]:
    videos_dict = [
        {
            "VIDEO_ID": item["id"],
            "TITLE": item["snippet"]["title"],
            "CHANNEL_ID": item["snippet"]["channelId"],
            "CHANNEL_TITLE": item["snippet"]["channelTitle"],
            "PUBLISHED_AT": extract_published(item["snippet"]["publishedAt"]),
            "CREATED_AT": created_at,
            "TAGS": item["snippet"].get("tags", []),
            "CATEGORY_ID": item["snippet"]["categoryId"],
            # 動画の長さ(P:YMWD, T:HMS)
            "DURATION": item["contentDetails"]["duration"],
            "VIEW_COUNT": int(item["statistics"].get("viewCount", 0)),
            "LIKE_COUNT": int(item["statistics"].get("likeCount", 0)),
            "DISLIKE_COUNT": int(item["statistics"].get("dislikeCount", 0)),
            "FAVORITE_COUNT": int(item["statistics"].get("favoriteCount", 0)),
            "COMMENT_COUNT": int(item["statistics"].get("commentCount", 0)),
        } for item in data["items"]
    ]

    return videos_dict
