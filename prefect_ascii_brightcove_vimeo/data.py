from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Any

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class AtedBy:
    type: str
    id: Optional[str] = None
    email: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class CustomFields:
    pass


class DeliveryType(Enum):
    DYNAMIC_ORIGIN = "dynamic_origin"
    STATIC_ORIGIN = "static_origin"
    UNKNOWN = "unknown"


class Economics(Enum):
    AD_SUPPORTED = "AD_SUPPORTED"


@dataclass_json
@dataclass(frozen=True)
class Source:
    src: str
    height: int
    width: int


@dataclass_json
@dataclass(frozen=True)
class Poster:
    src: str
    sources: List[Source]
    asset_id: Optional[str] = None
    remote: Optional[bool] = None


@dataclass_json
@dataclass(frozen=True)
class Images:
    poster: Optional[Poster] = None
    thumbnail: Optional[Poster] = None


class State(Enum):
    ACTIVE = "ACTIVE"


@dataclass_json
@dataclass(frozen=True)
class Video:
    id: str
    account_id: str
    complete: bool
    created_at: str
    created_by: AtedBy
    cue_points: List[Any]
    custom_fields: CustomFields
    delivery_type: DeliveryType
    duration: int
    economics: Economics
    has_digital_master: bool
    images: Images
    name: str
    published_at: str
    state: State
    tags: List[str]
    text_tracks: List[Any]
    updated_at: str
    updated_by: AtedBy
    link: Optional[str] = None
    geo: Optional[str] = None
    long_description: Optional[str] = None
    ad_keys: Optional[str] = None
    clip_source_video_id: Optional[str] = None
    schedule: Optional[str] = None
    sharing: Optional[str] = None
    description: Optional[str] = None
    digital_master_id: Optional[str] = None
    folder_id: Optional[str] = None
    original_filename: Optional[str] = None
    projection: Optional[str] = None
    reference_id: Optional[str] = None
    playback_rights_id: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
class VideoSource:
    uploaded_at: str
    src: str
    type: str
    ext_x_version: Optional[str] = None
    profiles: Optional[str] = None

    def is_mp4(self):
        return self.type.endswith('mp4')
