#%%
from googleapiclient.discovery import build
from api.youtube_api_config import YOUTUBE_API_KEY, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION
import json
from datetime import datetime
import pytz
import pathlib

class YoutubeApiRequest:
    def __init__(self) -> None:
        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=YOUTUBE_API_KEY
        )
        dt = datetime.now(pytz.timezone('Asia/Tokyo'))
        self.date_str = dt.strftime('%Y%m%d%H%M')
        self.output_path = list(pathlib.Path("/app/src").glob("json"))[0]
        
    def get_youtube_data_to_json(self):
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            chart="mostPopular",
            maxResults=50,
            regionCode="JP"
        )
        res = request.execute()
        
        with open(f"{self.output_path}/{self.date_str}_popular.json", encoding='utf-8', mode='w') as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
    
    # def get_youtube_most_popular(self):
    #     request = self.youtube.videos().list(
    #         part="snippet,contentDetails,statistics",
    #         chart="mostPopular",
    #         maxResults=50,
    #         regionCode="JP"
    #     )
    #     res = request.execute()
    #     videos = [
    #     {
    #         "video_id": item["id"],
    #         "title": item["snippet"]["title"],
    #         "published_at": item["snippet"]["publishedAt"],
    #         "tags": item["snippet"].get("tags", ""),
    #         "category_id": item["snippet"]["categoryId"],
    #         "duration": item["contentDetails"]["duration"], # 動画の長さ(P:YMWD, T:HMS)
    #         "view_count": item["statistics"]["viewCount"],
    #         "like_count": item["statistics"].get("likeCount", 0),
    #         "dislike_count": item["statistics"].get("dislikeCount", 0),
    #         "favorite_count": item["statistics"].get("favoriteCount", 0),
    #         "comment_count": item["statistics"].get("commentCount", 0),
    #     } for item in res["items"]
    #     ]
    #     return videos

    # def get_youtube_categories(self):
    #     request = self.youtube.videoCategories().list(
    #         part="id, snippet",
    #         regionCode="JP"
    #     )
    #     res = request.execute()
    #     categories = [
    #     {
    #         "id": item["id"], 
    #         "category": item["snippet"]["title"]
    #     } for item in res["items"] if item["snippet"]["assignable"]
    #     ]
    #     return categories
    

        
        


# %%
if __name__ == "__main__":
    youtube = YoutubeApiRequest()
    youtube.get_youtube_data_to_json()
# %%
