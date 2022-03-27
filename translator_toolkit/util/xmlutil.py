#!/usr/bin/env python3
import os
import re
from lxml import etree
from typing import Union


def get_parser(xml_file: str, encoding: Union[str, None] = None) -> etree.XMLParser:
    size_mb = os.path.getsize(xml_file) / 1000000
    if size_mb > 9:
        parser = etree.XMLParser(huge_tree=True, encoding=encoding)
    else:
        parser = etree.XMLParser(encoding=encoding)
    return parser


def remove_invalid_chars(chars):
    if not chars:
        return chars
    return re.sub(r'&#x.+?;', ' ', chars, flags=re.IGNORECASE)


def remove_outer_tags(xml: str) -> str:
    return re.sub(r'(^<[^<>]*?/?>)|(</[^<>]*?>$)', '', xml)


def tostring(elem: etree._Element) -> str:
    xml = etree.tostring(elem, encoding='unicode', with_tail=False)
    return remove_outer_tags(xml)
