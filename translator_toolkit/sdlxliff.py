#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import datetime
from typing import Iterator, Optional

from lxml import etree

from translator_toolkit.ns import XLF, SDLXLF
from translator_toolkit.util import xmlutil, stringutil
from translator_toolkit.error import TranslatorToolkitError
from translator_toolkit.xjson import XUnit, XGroup, XFile, XDocument


class SdlxliffComment(object):
    severity: str
    user: str
    date: Optional[datetime]
    version: str
    text: str

    def __init__(self, severity: str, user: str, date: Optional[datetime], version: str, text: str):
        self.severity = severity
        self.user = user
        self.date = date
        self.version = version
        self.text = text

    @classmethod
    def from_element(cls, elem: etree._Element) -> SdlxliffComment:
        severity = elem.get('severity', '')
        user = elem.get('user', '')
        date = stringutil.isoformat_to_datetime(elem.get('date', ''))
        version = elem.get('version', '')
        text = elem.text or ''
        comment = SdlxliffComment(severity, user, date, version, text)
        return comment


class SdlxliffCommentDefinition(object):
    id: str
    comments: list[SdlxliffComment]

    def __init__(self, id_: str, comments: list[SdlxliffComment]):
        self.id = id_
        self.comments = comments

    @classmethod
    def from_element(cls, elem: etree._Element) -> SdlxliffCommentDefinition:
        id_ = elem.get('id', '')
        comments = [SdlxliffComment.from_element(e) for e in elem.iterdescendants(SDLXLF + 'Comment')]
        comment_def = SdlxliffCommentDefinition(id_, comments)
        return comment_def


class SdlxliffSegmentPair(object):
    mid: str
    source: str
    target: str

    def __init__(self, mid: str, source: str, target: str):
        self.mid = mid
        self.source = source
        self.target = target

    @staticmethod
    def from_element(src_mrk: etree._Element, tgt_mrk: etree._Element) -> SdlxliffSegmentPair:
        mid = src_mrk.get('mid', '').replace('_x0020_', ' ')
        source = xmlutil.tostring(src_mrk)
        target = xmlutil.tostring(tgt_mrk)
        pair = SdlxliffSegmentPair(mid, source, target)
        return pair

    def get_comment_ids(self) -> Iterator[str]:
        for m in re.finditer(r'sdl:cid="(.+?)"', self.source):
            yield m.group(1)
        for m in re.finditer(r'sdl:cid="(.+?)"', self.target):
            yield m.group(1)

    def to_json(self, srclang: str, tgtlang: str) -> XUnit:
        obj: XUnit = {
            'id': self.mid,
            'source': self.source,
            'target': self.target,
            'srclang': srclang,
            'tgtlang': tgtlang,
            'properties': None
        }
        return obj


class SdlxliffSegDefinition(object):
    id: str
    conf: str
    origin: str
    origin_system: str
    percent: float
    locked: bool

    def __init__(self, id_: str, conf: str, origin: str, origin_system: str, percent: float, locked: bool):
        self.id = id_
        self.conf = conf
        self.origin = origin
        self.origin_system = origin_system
        self.percent = percent
        self.locked = locked

    @classmethod
    def from_element(cls, elem: etree._Element) -> SdlxliffSegDefinition:
        id_ = elem.get('id', '')
        conf = elem.get('conf', '')
        origin = elem.get('origin', '')
        origin_system = elem.get('origin-system', '')
        v = elem.get('percent', '0')
        percent = float(v) if stringutil.is_float(v) else 0.0
        locked = elem.get('locked', 'false') == 'true'
        seg_def = SdlxliffSegDefinition(id_, conf, origin, origin_system, percent, locked)
        return seg_def


class SdlxliffTransUnit(object):
    id: str
    segment_pairs: list[SdlxliffSegmentPair]
    segment_definitions: list[SdlxliffSegDefinition]

    def __init__(self, id_: str, segment_pairs: list[SdlxliffSegmentPair], segment_definitions: list[SdlxliffSegDefinition]):
        self.id = id_
        self.segment_pairs = segment_pairs
        self.segment_definitions = segment_definitions

    @classmethod
    def from_element(cls, elem: etree._Element) -> SdlxliffTransUnit:
        id_ = elem.get('id', '')
        segment_pairs = []
        segment_definitions = []
        seg_source = elem.find(f'./{XLF}seg-source')
        target = elem.find(f'./{XLF}target')
        if seg_source is not None and target is not None:
            src_mrks = (e for e in seg_source.iterchildren(XLF + 'mrk') if e.get('mtype') == 'seg')
            tgt_mrks = (e for e in target.iterchildren(XLF + 'mrk') if e.get('mtype') == 'seg')
            for src_mrk, tgt_mrk in zip(src_mrks, tgt_mrks):
                pair = SdlxliffSegmentPair.from_element(src_mrk, tgt_mrk)
                segment_pairs.append(pair)
        seg_defs = elem.find(f'./{SDLXLF}seg-defs')
        if seg_defs is not None:
            for seg in seg_defs.iterchildren(SDLXLF + 'seg'):
                seg_def = SdlxliffSegDefinition.from_element(seg)
                segment_definitions.append(seg_def)
        tu = SdlxliffTransUnit(id_, segment_pairs, segment_definitions)
        return tu

    def get_segment_definition(self, mid: str) -> Optional[SdlxliffSegDefinition]:
        seg_def = next((seg_def for seg_def in self.segment_definitions if seg_def.id == mid), None)
        return seg_def

    def to_json(self, srclang: str, tgtlang: str) -> XGroup:
        obj: XGroup = {
            'id': self.id,
            'name': 'trans-unit',
            'units': [x.to_json(srclang, tgtlang) for x in self.segment_pairs],
            'properties': None
        }
        return obj


class SdlxliffBody(object):
    trans_units: list[SdlxliffTransUnit]

    def __init__(self, trans_units: list[SdlxliffTransUnit]):
        self.trans_units = trans_units

    @classmethod
    def from_element(cls, elem: etree._Element) -> SdlxliffBody:
        trans_units = [SdlxliffTransUnit.from_element(e) for e in elem.iterdescendants(XLF + 'trans-unit')]
        obj = SdlxliffBody(trans_units)
        return obj


class SdlxliffFile(object):
    source_language: str
    target_language: str
    original: str
    datatype: str
    body: SdlxliffBody

    def __init__(self, source_language: str, target_language: str, original: str, datatype: str, body: SdlxliffBody):
        self.source_language = source_language
        self.target_language = target_language
        self.original = original
        self.datatype = datatype
        self.body = body

    @classmethod
    def from_element(cls, elem: etree._Element) -> SdlxliffFile:
        original = elem.get('original', '')
        datatype = elem.get('datatype', '')
        source_language = elem.get('source-language', '')
        target_language = elem.get('target-language', '')
        body_elem = elem.find(f'./{XLF}body')
        if body_elem is None:
            raise TranslatorToolkitError('body element not found')
        body = SdlxliffBody.from_element(body_elem)
        obj = SdlxliffFile(source_language, target_language, original, datatype, body)
        return obj

    def to_json(self) -> XFile:
        obj: XFile = {
            'srclang': self.source_language,
            'tgtlang': self.target_language,
            'groups': [g.to_json(self.source_language, self.target_language) for g in self.body.trans_units],
            'properties': {
                'original': self.original,
                'datatype': self.datatype
            }
        }
        return obj


class SdlxliffDocInfo(object):
    comment_definitions: list[SdlxliffCommentDefinition]

    def __init__(self, comment_definitions: list[SdlxliffCommentDefinition]):
        self.comment_definitions = comment_definitions

    @classmethod
    def from_element(cls, elem: etree._Element) -> SdlxliffDocInfo:
        comment_definitions = []
        for cmt_defs_elem in elem.iterchildren(SDLXLF + 'cmt-defs'):
            for cmt_def_elem in cmt_defs_elem.iterchildren(SDLXLF + 'cmt-def'):
                cmt_def = SdlxliffCommentDefinition.from_element(cmt_def_elem)
                comment_definitions.append(cmt_def)

        doc_info = SdlxliffDocInfo(comment_definitions)
        return doc_info

    def get_comments(self, cid: str) -> Iterator[SdlxliffComment]:
        for comment_def in [comment_def for comment_def in self.comment_definitions if comment_def.id == cid]:
            for comment in comment_def.comments:
                yield comment


class Sdlxliff(object):
    source_file: str
    doc_info: SdlxliffDocInfo
    files: list[SdlxliffFile]

    def __init__(self, source_file: str, doc_info: SdlxliffDocInfo, files: list[SdlxliffFile]):
        self.source_file = source_file
        self.doc_info = doc_info
        self.files = files

    @classmethod
    def load_valid_xml_string(cls, source_file: str) -> str:
        lines = []
        with open(source_file) as infile:
            for line in infile:
                lines.append(xmlutil.remove_invalid_chars(line))

        xml_string = ''.join(lines)
        return xml_string

    @classmethod
    def load(cls, source_file: str) -> Sdlxliff:
        xml_string = Sdlxliff.load_valid_xml_string(source_file)
        parser = xmlutil.get_parser(source_file, encoding='utf-8')
        root = etree.fromstring(xml_string.encode('utf-8'), parser=parser)

        doc_info_elem = root.find(f'./{SDLXLF}doc-info')
        if doc_info_elem is None:
            raise TranslatorToolkitError('doc-info element not found')
        doc_info = SdlxliffDocInfo.from_element(doc_info_elem)

        files = [SdlxliffFile.from_element(e) for e in root.iterchildren(XLF + 'file')]
        sdlxliff = Sdlxliff(source_file, doc_info, files)
        return sdlxliff

    def to_json(self) -> XDocument:
        obj: XDocument = {
            'source_file': self.source_file,
            'files': [f.to_json() for f in self.files],
            'properties': None
        }
        return obj

    def get_all_trans_units(self) -> Iterator[SdlxliffTransUnit]:
        for file in self.files:
            for tu in file.body.trans_units:
                yield tu

    def get_all_segment_pairs(self) -> Iterator[SdlxliffSegmentPair]:
        for file in self.files:
            for tu in file.body.trans_units:
                for sp in tu.segment_pairs:
                    yield sp

    @property
    def source_language(self):
        return self.files[0].source_language if self.files else ''

    @property
    def target_language(self):
        return self.files[0].target_language if self.files else ''
