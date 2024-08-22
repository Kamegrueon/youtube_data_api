from typing import Any

from api.schemas import YouTubeVideoResponse


def extract_published(published_at: str) -> str:
    date = published_at[0:10]
    time = published_at[11:16]
    return f"{date} {time}:00"


def extract_most_popular(data: YouTubeVideoResponse, created_at: str) -> list[dict[str, Any]]:
    videos_dict = [
        {
            "VIDEO_ID": item["id"],
            "TITLE": item["snippet"]["title"] if item["snippet"] else "",
            "CHANNEL_ID": item["snippet"]["channelId"] if item["snippet"] else "",
            "CHANNEL_TITLE": item["snippet"]["channelTitle"] if item["snippet"] else "",
            "PUBLISHED_AT": extract_published(item["snippet"]["publishedAt"] if item["snippet"] else ""),
            "CREATED_AT": created_at,
            "TAGS": item["snippet"].get("tags", []) if item["snippet"] else "",
            "CATEGORY_ID": item["snippet"]["categoryId"] if item["snippet"] else "",
            # 動画の長さ(P:YMWD, T:HMS)
            "DURATION": item["contentDetails"]["duration"] if item["contentDetails"] else "",
            "VIEW_COUNT": int(item["statistics"].get("viewCount", 0)) if item["statistics"] else None,
            "LIKE_COUNT": int(item["statistics"].get("likeCount", 0)) if item["statistics"] else None,
            "DISLIKE_COUNT": int(item["statistics"].get("dislikeCount", 0)) if item["statistics"] else None,
            "FAVORITE_COUNT": int(item["statistics"].get("favoriteCount", 0)) if item["statistics"] else None,
            "COMMENT_COUNT": int(item["statistics"].get("commentCount", 0)) if item["statistics"] else None,
        }
        for item in data["items"]
    ]

    return videos_dict
