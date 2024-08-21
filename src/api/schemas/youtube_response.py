from typing import Optional, TypedDict


class pageInfo(TypedDict):
    totalResults: int
    resultsPerPage: int


class Thumbnail(TypedDict):
    url: str
    width: Optional[int]
    height: Optional[int]


class Thumbnails(TypedDict):
    default: Optional[Thumbnail]
    medium: Optional[Thumbnail]
    high: Optional[Thumbnail]
    standard: Optional[Thumbnail]
    maxres: Optional[Thumbnail]


class Localized(TypedDict):
    title: str
    description: str


class Snippet(TypedDict):
    publishedAt: str
    channelId: str
    title: str
    description: str
    thumbnails: Thumbnails
    channelTitle: str
    categoryId: str
    liveBroadcastContent: str
    localized: Localized
    defaultAudioLanguage: Optional[str]


class ContentDetails(TypedDict):
    duration: str
    dimension: str
    definition: str
    caption: str
    licensedContent: bool
    contentRating: str
    projection: str


class Statistics(TypedDict):
    viewCount: str
    likeCount: str
    favoriteCount: str
    commentCount: str


class YouTubeVideoItems(TypedDict):
    kind: str
    etag: str
    id: str
    snippet: Optional[Snippet]
    contentDetails: Optional[ContentDetails]
    statistics: Optional[Statistics]


class YouTubeVideoResponse(TypedDict):
    kind: str
    etag: str
    items: list[YouTubeVideoItems]
    nextPageToken: Optional[str]
    prevPageToken: Optional[str]
    pageInfo: pageInfo
