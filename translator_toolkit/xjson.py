#!/usr/bin/env python3
from typing import TypedDict, Optional


class XUnit(TypedDict):
    id: str
    source: str
    target: str
    srclang: str
    tgtlang: str
    properties: Optional[dict]


class XGroup(TypedDict):
    id: str
    name: str
    units: list[XUnit]
    properties: Optional[dict]


class XFile(TypedDict):
    srclang: str
    tgtlang: str
    groups: list[XGroup]
    properties: Optional[dict]


class XDocument(TypedDict):
    source_file: str
    files: list[XFile]
    properties: Optional[dict]
