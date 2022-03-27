#!/usr/bin/env python3
from __future__ import annotations
from typing import Iterator
from datetime import datetime
from lxml import etree

from translator_toolkit.error import TranslatorToolkitError
from translator_toolkit.ns import XLF, MXLF
from translator_toolkit.util import xmlutil, stringutil
from translator_toolkit.xjson import XUnit, XGroup, XFile, XDocument


class MxliffAltTrans(object):
    match_quality: float
    origin: str
    target: str

    def __init__(self, origin: str, match_quality: float, target: str):
        self.origin = origin
        self.match_quality = match_quality
        self.target = target

    @classmethod
    def from_element(cls, elem: etree._Element) -> MxliffAltTrans:
        origin = elem.get('origin', '')
        v = elem.get('match-quality', '0')
        match_quality = float(v) if stringutil.is_float(v) else 0
        target_elem = elem.find(f'./{XLF}target')
        target = target_elem.text or '' if target_elem is not None else ''
        obj = MxliffAltTrans(origin, match_quality, target)
        return obj


class MxliffTransUnit(object):
    id: str
    source: str
    target: str
    m_trans_origin: str
    m_score: float
    m_gross_score: float
    m_confirmed: str
    m_locked: bool
    m_para_id: str
    m_created_at: datetime
    m_created_by: str
    m_modified_at: datetime
    m_modified_by: str
    m_level_edited: bool
    alt_trans_units: list[MxliffAltTrans]

    def __init__(self, id_: str, source: str, target: str, m_trans_origin: str, m_score: float, m_gross_score: float,
                 m_confirmed: str, m_locked: bool, m_para_id: str, m_created_at: datetime, m_created_by: str,
                 m_modified_at: datetime, m_modified_by: str, m_level_edited: bool, alt_trans_units: list[MxliffAltTrans]):
        self.id = id_
        self.source = source
        self.target = target
        self.m_trans_origin = m_trans_origin
        self.m_score = m_score
        self.m_gross_score = m_gross_score
        self.m_confirmed = m_confirmed
        self.m_locked = m_locked
        self.m_para_id = m_para_id
        self.m_created_at = m_created_at
        self.m_created_by = m_created_by
        self.m_modified_at = m_modified_at
        self.m_modified_by = m_modified_by
        self.m_level_edited = m_level_edited
        self.alt_trans_units = alt_trans_units

    @classmethod
    def from_element(cls, elem: etree._Element) -> MxliffTransUnit:
        id_ = elem.get('id', '')
        m_trans_origin = elem.get(MXLF + 'trans-origin', '')
        m_confirmed = elem.get(MXLF + 'confirmed', '')
        m_locked = True if elem.get(MXLF + 'locked') != 'false' else False
        v = elem.get(MXLF + 'score', '0')
        m_score = float(v) if stringutil.is_float(v) else 0
        v = elem.get(MXLF + 'gross-score', '0')
        m_gross_score = float(v) if stringutil.is_float(v) else 0
        m_para_id = elem.get(MXLF + 'para-id', '')

        v = elem.get(MXLF + 'created-at', '0')
        m_created_at = stringutil.unixtime_to_datetime(v)

        m_created_by = elem.get(MXLF + 'created-by', '')

        v = elem.get(MXLF + 'modified-at', '0')
        m_modified_at = stringutil.unixtime_to_datetime(v)

        m_modified_by = elem.get(MXLF + 'modified-by', '')
        m_level_edited = elem.get(MXLF + 'level-edited') == 'true'

        source_elem = elem.find(f'./{XLF}source')
        target_elem = elem.find(f'./{XLF}target')
        source = source_elem.text or '' if source_elem is not None else ''
        target = target_elem.text or '' if target_elem is not None else ''

        alt_trans_units = [MxliffAltTrans.from_element(e) for e in elem.iterchildren(XLF + 'alt-trans')]

        obj = MxliffTransUnit(id_, source, target, m_trans_origin, m_score, m_gross_score, m_confirmed, m_locked,
                              m_para_id, m_created_at, m_created_by, m_modified_at, m_modified_by, m_level_edited,
                              alt_trans_units)
        return obj

    def to_json(self, srclang: str, tgtlang: str) -> XUnit:
        obj: XUnit = {
            'id': self.id,
            'source': self.source,
            'target': self.target,
            'srclang': srclang,
            'tgtlang': tgtlang,
            'properties': None
        }
        return obj


class MxliffContext(object):
    context_type: str
    value: str

    def __init__(self, context_type: str, value: str):
        self.context_type = context_type
        self.value = value

    @classmethod
    def from_element(cls, elem: etree._Element) -> MxliffContext:
        context_type = elem.get('context_type', '')
        value = elem.text or ''
        obj = MxliffContext(context_type, value)
        return obj


class MxliffContextGroup(object):
    contexts: list[MxliffContext]

    def __init__(self, contexts: list[MxliffContext]):
        self.contexts = contexts

    @classmethod
    def from_element(cls, elem: etree._Element) -> MxliffContextGroup:
        contexts = [MxliffContext.from_element(e) for e in elem.iterchildren(XLF + 'context')]
        obj = MxliffContextGroup(contexts)
        return obj


class MxliffGroup(object):
    id: str
    m_para_id: str
    context_groups: list[MxliffContextGroup]
    trans_units: list[MxliffTransUnit]

    def __init__(self, id_: str, m_para_id: str, context_groups: list[MxliffContextGroup],
                 trans_units: list[MxliffTransUnit]):
        self.id = id_
        self.m_para_id = m_para_id
        self.context_groups = context_groups
        self.trans_units = trans_units

    @classmethod
    def from_element(cls, elem: etree._Element) -> MxliffGroup:
        id_ = elem.get('id', '')
        m_para_id = elem.get(MXLF + 'para-id', '')
        context_groups = [MxliffContextGroup.from_element(e) for e in elem.iterchildren(XLF + 'context-group')]
        trans_units = [MxliffTransUnit.from_element(e) for e in elem.iterchildren(XLF + 'trans-unit')]
        obj = MxliffGroup(id_, m_para_id, context_groups, trans_units)
        return obj

    def to_json(self, srclang: str, tgtlang: str) -> XGroup:
        obj: XGroup = {
            'id': self.id,
            'name': 'group',
            'units': [tu.to_json(srclang, tgtlang) for tu in self.trans_units],
            'properties': None
        }
        return obj


class MxliffBody(object):
    gruops: list[MxliffGroup]

    def __init__(self, groups: list[MxliffGroup]):
        self.gruops = groups

    @classmethod
    def from_element(cls, elem: etree._Element) -> MxliffBody:
        groups = [MxliffGroup.from_element(e) for e in elem.iterchildren(XLF + 'group')]
        obj = MxliffBody(groups)
        return obj


class MxliffFile(object):
    source_language: str
    target_language: str
    original: str
    datatype: str
    m_file_format: str
    m_task_id: str
    body: MxliffBody

    def __init__(self, source_language: str, target_language: str, original: str, datatype: str, m_file_format: str,
                 m_task_id: str, body: MxliffBody):
        self.source_language = source_language
        self.target_language = target_language
        self.original = original
        self.datatype = datatype
        self.m_file_format = m_file_format
        self.m_task_id = m_task_id
        self.body = body

    @classmethod
    def from_element(cls, elem: etree._Element) -> MxliffFile:
        original = elem.get('original', '')
        datatype = elem.get('datatype', '')
        source_language = elem.get('source-language', '')
        target_language = elem.get('target-language', '')
        m_file_format = elem.get(MXLF + 'file-format', '')
        m_task_id = elem.get(MXLF + 'task-id', '')

        body_elem = elem.find(f'./{XLF}body')
        if body_elem is None:
            raise TranslatorToolkitError('body element not found')
        body = MxliffBody.from_element(body_elem)

        obj = MxliffFile(source_language, target_language, original, datatype, m_file_format, m_task_id, body)
        return obj

    def to_json(self) -> XFile:
        obj: XFile = {
            'srclang': self.source_language,
            'tgtlang': self.target_language,
            'groups': [g.to_json(self.source_language, self.target_language) for g in self.body.gruops],
            'properties': {
                'original': self.original,
                'datatype': self.m_file_format
            }
        }
        return obj


class Mxliff(object):
    source_file: str
    level: int
    version: str
    m_version: str
    files: list[MxliffFile]

    def __init__(self, source_file: str, level: int, version: str, m_version: str, files: list[MxliffFile]):
        self.source_file = source_file
        self.level = level
        self.version = version
        self.m_version = m_version
        self.files = files

    @classmethod
    def load(cls, source_file: str) -> Mxliff:
        parser = xmlutil.get_parser(source_file)
        root = etree.parse(source_file, parser=parser).getroot()
        level = int(root.get(MXLF + 'level', 1))
        version = root.get('version', '')
        m_version = root.get(MXLF + 'version', '')
        files = [MxliffFile.from_element(e) for e in root.iterchildren(XLF + 'file')]
        obj = Mxliff(source_file, level, version, m_version, files)

        return obj

    def to_json(self) -> XDocument:
        obj: XDocument = {
            'source_file': self.source_file,
            'files': [f.to_json() for f in self.files],
            'properties': None
        }
        return obj

    def get_all_trans_units(self) -> Iterator[MxliffTransUnit]:
        for file in self.files:
            for group in file.body.gruops:
                for tu in group.trans_units:
                    yield tu

    @property
    def source_language(self):
        return self.files[0].source_language if self.files else ''

    @property
    def target_language(self):
        return self.files[0].target_language if self.files else ''
