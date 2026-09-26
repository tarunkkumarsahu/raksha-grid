from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class GeoJSONFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: dict
    properties: dict = Field(default_factory=dict)


class GeoJSONFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[GeoJSONFeature] = Field(min_length=1, max_length=25_000)
    replace_existing: bool = False
