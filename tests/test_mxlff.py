#!/usr/bin/env python3
import os
from translator_toolkit.mxliff import Mxliff
from translator_toolkit.util import stringutil

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def test_load():
    file = os.path.join(data_dir, '01_ja-ja-en-R.mxliff')
    mxlf = Mxliff.load(file)
    assert mxlf.source_language == 'ja'
    assert mxlf.target_language == 'en'
    assert mxlf.version == '1.2'
    assert mxlf.m_version == '2.4'
    assert mxlf.level == 2

    assert len(mxlf.files) == 1

    mfile0 = mxlf.files[0]
    assert mfile0.source_language == 'ja'
    assert mfile0.target_language == 'en'
    assert mfile0.original == '01_ja.docx'
    assert mfile0.datatype == 'x-undefined'
    assert mfile0.m_file_format == 'DOC'
    assert mfile0.m_task_id == 'stbZWjwCihfeyJzn_dc5'

    assert len(mfile0.body.gruops) == 2

    mgroup0 = mfile0.body.gruops[0]
    assert mgroup0.id == '0'
    assert mgroup0.m_para_id == '0'

    mgroup1 = mfile0.body.gruops[1]
    assert mgroup1.id == '1'
    assert mgroup1.m_para_id == '0'

    assert len(mgroup0.trans_units) == 1
    assert mgroup0.trans_units[0].id == '0'
    assert mgroup0.trans_units[0].m_score == 0.0
    assert mgroup0.trans_units[0].m_gross_score == 0.0
    assert mgroup0.trans_units[0].m_trans_origin == 'null'
    assert mgroup0.trans_units[0].m_confirmed == '2'
    assert not mgroup0.trans_units[0].m_locked
    assert mgroup0.trans_units[0].m_para_id == '0'
    assert mgroup0.trans_units[0].m_created_at == stringutil.unixtime_to_datetime('1580950266722')
    assert mgroup0.trans_units[0].m_created_by == '232275'
    assert mgroup0.trans_units[0].m_modified_at == stringutil.unixtime_to_datetime('1580950876561')
    assert mgroup0.trans_units[0].m_modified_by == '5911'
    assert mgroup0.trans_units[0].m_level_edited
    assert mgroup0.trans_units[0].source == 'AAAA'
    assert mgroup0.trans_units[0].target == 'BBBB'

    malt_trans_units = mgroup0.trans_units[0].alt_trans_units
    assert len(malt_trans_units) == 2
    assert malt_trans_units[0].target == 'CCCC'
    assert malt_trans_units[0].origin == 'machine-trans'
    assert malt_trans_units[0].match_quality == 0.0
    assert malt_trans_units[1].target == ''
    assert malt_trans_units[1].origin == 'memsource-tm'
    assert malt_trans_units[1].match_quality == 0.0

    assert len(mgroup1.trans_units) == 1
    assert mgroup1.trans_units[0].id == '1'
    assert mgroup1.trans_units[0].m_score == 90.9
    assert mgroup1.trans_units[0].m_gross_score == 90.0
    assert mgroup1.trans_units[0].m_trans_origin == 'tm'
    assert mgroup1.trans_units[0].m_confirmed == '0'
    assert mgroup1.trans_units[0].m_locked
    assert mgroup1.trans_units[0].m_para_id == '0'
    assert mgroup1.trans_units[0].m_created_at == stringutil.unixtime_to_datetime('1580950272298')
    assert mgroup1.trans_units[0].m_created_by == '232275'
    assert mgroup1.trans_units[0].m_modified_at == stringutil.unixtime_to_datetime('1580950876561')
    assert mgroup1.trans_units[0].m_modified_by == '5911'
    assert mgroup1.trans_units[0].m_level_edited
    assert mgroup1.trans_units[0].source == 'DDDD'
    assert mgroup1.trans_units[0].target == 'EEEE'

    malt_trans_units = mgroup1.trans_units[0].alt_trans_units
    assert len(malt_trans_units) == 2
    assert malt_trans_units[0].target == 'FFFF'
    assert malt_trans_units[0].origin == 'machine-trans'
    assert malt_trans_units[0].match_quality == 0.0
    assert malt_trans_units[1].target == 'GGGG'
    assert malt_trans_units[1].origin == 'memsource-tm'
    assert malt_trans_units[1].match_quality == 75.0


def test_to_json():
    file = os.path.join(data_dir, '01_ja-ja-en-R.mxliff')
    mxlf = Mxliff.load(file)
    xdoc = mxlf.to_json()

    assert xdoc['source_file'] == file
    assert len(xdoc['files']) == 1

    xfile = xdoc['files'][0]
    assert xfile['srclang'] == 'ja'
    assert xfile['tgtlang'] == 'en'
    assert xfile['properties']['original'] == '01_ja.docx'
    assert xfile['properties']['datatype'] == 'DOC'
    assert len(xfile['groups']) == 2

    xgroups = xfile['groups']

    xgroup0 = xgroups[0]
    assert xgroup0['id'] == '0'
    assert xgroup0['name'] == 'group'
    assert len(xgroup0['units']) == 1

    xunit0 = xgroup0['units'][0]
    assert xunit0['id'] == '0'
    assert xunit0['source'] == 'AAAA'
    assert xunit0['target'] == 'BBBB'
    assert xunit0['srclang'] == 'ja'
    assert xunit0['tgtlang'] == 'en'

    xgroup1 = xgroups[1]
    assert xgroup1['id'] == '1'
    assert xgroup1['name'] == 'group'
    assert len(xgroup1['units']) == 1

    xunit1 = xgroup1['units'][0]
    assert xunit1['id'] == '1'
    assert xunit1['source'] == 'DDDD'
    assert xunit1['target'] == 'EEEE'
    assert xunit1['srclang'] == 'ja'
    assert xunit1['tgtlang'] == 'en'
