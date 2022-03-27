#!/usr/bin/env python3
import os
from translator_toolkit.sdlxliff import Sdlxliff
from datetime import datetime

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def test_load():
    file = os.path.join(data_dir, 'merged.docx.sdlxliff')
    sxlf = Sdlxliff.load(file)
    assert sxlf.source_language == 'ja-JP'
    assert sxlf.target_language == 'en-us'
    assert sxlf.source_file == file

    assert len(sxlf.files) == 2

    sfile0 = sxlf.files[0]
    assert sfile0.source_language == 'ja-JP'
    assert sfile0.target_language == 'en-us'
    assert sfile0.original == 'test1.docx'
    assert sfile0.datatype == 'x-sdlfilterframework2'

    tunits0 = sfile0.body.trans_units
    assert len(tunits0) == 2

    segment_pairs0 = [{'mid': x.mid, 'source': x.source, 'target': x.target} for x in tunits0[0].segment_pairs]
    assert segment_pairs0 == [
        {
            'mid': '1',
            'source': 'ビデオを使うと、伝えたい内容を明確に表現できます。',
            'target': '<mrk mtype="x-sdl-comment" sdl:cid="229d3377-d1c8-4419-a506-4f7ad7bf9d60"><mrk mtype="x-sdl-comment" sdl:cid="7990a264-9bb4-4c5e-8906-8d234f8497d8">'
            '<mrk mtype="x-sdl-comment" sdl:cid="e5011b5a-1970-473b-b94d-303dbad8058b">With videos</mrk>, '
            'you can clearly articulate</mrk></mrk> what you want to convey.'
        },
        {
            'mid': '2',
            'source': '[オンライン ビデオ] をクリックすると、追加したいビデオを、それに応じた埋め込みコードの形式で貼り付けできるようになります。',
            'target': 'Clicking Online Video will allow you to paste the video you want to add in the corresponding embed code.'
        },
        {
            'mid': '3',
            'source': 'キーワードを入力して、文書に最適なビデオをオンラインで検索することもできます。',
            'target': '<mrk mtype="x-sdl-comment" sdl:cid="af6deea3-97c0-4e9f-bcf5-2bf1b3635695">You can also enter keywords to search online for the best video for your document.</mrk>'
        }]

    seg_defs0 = [{'id': x.id, 'conf': x.conf, 'origin': x.origin, 'origin_system': x.origin_system, 'percent': x.percent, 'locked': x.locked} for x in tunits0[0].segment_definitions]
    assert seg_defs0 == [
        {
            'id': '1',
            'conf': 'Translated',
            'origin': 'mt',
            'origin_system': 'Google Cloud Translation API',
            'percent': 0.0,
            'locked': False
        },
        {
            'id': '2',
            'conf': 'Translated',
            'origin': 'mt',
            'origin_system': 'Google Cloud Translation API',
            'percent': 0.0,
            'locked': False
        },
        {
            'id': '3',
            'conf': 'Translated',
            'origin': 'mt',
            'origin_system': 'Google Cloud Translation API',
            'percent': 0.0,
            'locked': False
        }
    ]

    segment_pairs1 = [{'mid': x.mid, 'source': x.source, 'target': x.target} for x in tunits0[1].segment_pairs]
    assert segment_pairs1 == [
        {
            'mid': '4 a',
            'source': 'Word に用意されているヘッダー、フッター、表紙、テキスト ボックス デザインを組み合わせると、プロのようなできばえの文書を作成できます。',
            'target': 'Combine the header, footer, cover, and text box designs provided with Word to create professional-looking documents.'
        },
        {
            'mid': '4 b a',
            'source': 'たとえば、一致する表紙、ヘッダー、サイドバーを追加できます。',
            'target': 'For example, you can add matching covers, headers, and sidebars.'
        },
        {
            'mid': '4 b b a',
            'source': '[挿入] をクリックしてから、それぞれのギャラリーで目的の要素を選んでください。',
            'target': 'Click Insert, then select the desired element in each gallery.'
        },
        {
            'mid': '4 b b b',
            'source': 'テーマとスタイルを使って、文書全体の統一感を出すこともできます。',
            'target': 'You can also use themes and styles to create a sense of unity throughout the document.'
        },
    ]

    seg_defs1 = [{'id': x.id, 'conf': x.conf, 'origin': x.origin, 'origin_system': x.origin_system, 'percent': x.percent, 'locked': x.locked} for x in tunits0[1].segment_definitions]
    assert seg_defs1 == [
        {
            'id': '4 a',
            'conf': 'Translated',
            'origin': 'mt',
            'origin_system': 'Google Cloud Translation API',
            'percent': 0.0,
            'locked': False
        },
        {
            'id': '4 b a',
            'conf': 'Translated',
            'origin': 'mt',
            'origin_system': 'Google Cloud Translation API',
            'percent': 0.0,
            'locked': False
        },
        {
            'id': '4 b b a',
            'conf': 'Translated',
            'origin': 'mt',
            'origin_system': 'Google Cloud Translation API',
            'percent': 0.0,
            'locked': False
        },
        {
            'id': '4 b b b',
            'conf': 'Translated',
            'origin': 'mt',
            'origin_system': 'Google Cloud Translation API',
            'percent': 0.0,
            'locked': False
        }
    ]

    sfile1 = sxlf.files[1]
    assert sfile1.source_language == 'ja-JP'
    assert sfile1.target_language == 'en-us'
    assert sfile1.original == 'test2.docx'
    assert sfile1.datatype == 'x-sdlfilterframework2'

    tunits1 = sfile1.body.trans_units
    assert len(tunits1) == 2

    segment_pairs1_0 = [{'mid': x.mid, 'source': x.source, 'target': x.target} for x in tunits1[0].segment_pairs]
    assert segment_pairs1_0 == [
        {
            'mid': '16',
            'source': 'ビデオを使うと、伝えたい内容を明確に表現できます。',
            'target': 'With videos, you can clearly articulate what you want to convey.'
        },
        {
            'mid': '17',
            'source': '[オンライン ビデオ] をクリックすると、追加したいビデオを、それに応じた埋め込みコードの形式で貼り付けできるようになります。',
            'target': 'Clicking Online Video will allow you to paste the video you want to add in the corresponding embed code.'
        },
        {
            'mid': '18',
            'source': 'キーワードを入力して、文書に最適なビデオをオンラインで検索することもできます。',
            'target': 'You can also enter keywords to search online for the best video for your document.'
        }]

    seg_defs1_0 = [{'id': x.id, 'conf': x.conf, 'origin': x.origin, 'origin_system': x.origin_system, 'percent': x.percent, 'locked': x.locked} for x in tunits1[0].segment_definitions]
    assert seg_defs1_0 == [
        {
            'id': '16',
            'conf': 'Translated',
            'origin': 'auto-propagated',
            'origin_system': 'Propagated from segment 1',
            'percent': 100.0,
            'locked': False
        },
        {
            'id': '17',
            'conf': 'Translated',
            'origin': 'auto-propagated',
            'origin_system': 'Propagated from segment 2',
            'percent': 100.0,
            'locked': False
        },
        {
            'id': '18',
            'conf': 'Translated',
            'origin': 'auto-propagated',
            'origin_system': 'Propagated from segment 3',
            'percent': 100.0,
            'locked': False
        }
    ]
    segment_pairs1_1 = [{'mid': x.mid, 'source': x.source, 'target': x.target} for x in tunits1[1].segment_pairs]
    assert segment_pairs1_1 == [
        {
            'mid': '19',
            'source': 'Word に用意されているヘッダー、フッター、表紙、テキスト ボックス デザインを組み合わせると、プロのようなできばえの文書を作成できます。',
            'target': 'Combine the header, footer, cover, and text box designs provided with Word to create professional-looking documents.'
        },
        {
            'mid': '20',
            'source': 'たとえば、一致する表紙、ヘッダー、サイドバーを追加できます。',
            'target': 'For example, you can add matching covers, headers, and sidebars.'
        },
        {
            'mid': '21',
            'source': '[挿入] をクリックしてから、それぞれのギャラリーで目的の要素を選んでください。',
            'target': 'Click Insert, then select the desired element in each gallery.'
        }]

    seg_defs1_1 = [{'id': x.id, 'conf': x.conf, 'origin': x.origin, 'origin_system': x.origin_system, 'percent': x.percent, 'locked': x.locked} for x in tunits1[1].segment_definitions]
    assert seg_defs1_1 == [
        {
            'id': '19',
            'conf': 'Translated',
            'origin': 'auto-propagated',
            'origin_system': 'Propagated from segment 4 a',
            'percent': 100.0,
            'locked': False
        },
        {
            'id': '20',
            'conf': 'Translated',
            'origin': 'auto-propagated',
            'origin_system': 'Propagated from segment 4 b a',
            'percent': 100.0,
            'locked': False
        },
        {
            'id': '21',
            'conf': 'Translated',
            'origin': 'auto-propagated',
            'origin_system': 'Propagated from segment 4 b b a',
            'percent': 100.0,
            'locked': False
        }
    ]

    comment_defs = sxlf.doc_info.comment_definitions
    assert len(comment_defs) == 5
    assert len(comment_defs[0].comments) == 2
    assert comment_defs[0].comments[0].text == 'Comment1'
    assert comment_defs[0].comments[0].severity == 'Low'
    assert comment_defs[0].comments[0].user == 'testuser'
    assert comment_defs[0].comments[0].version == '1.0'
    assert isinstance(comment_defs[0].comments[0].date, datetime)

    assert comment_defs[0].comments[1].text == 'Comment 3\nABC'
    assert comment_defs[0].comments[1].severity == 'Low'
    assert comment_defs[0].comments[1].user == 'testuser'
    assert comment_defs[0].comments[1].version == '2.0'
    assert isinstance(comment_defs[0].comments[1].date, datetime)

    cid = comment_defs[0].id
    comments = [c for c in sxlf.doc_info.get_comments(cid)]
    assert len(comments) == 2
    assert comments[0].text == comment_defs[0].comments[0].text
    assert comments[1].text == comment_defs[0].comments[1].text


def test_to_json():
    file = os.path.join(data_dir, 'merged.docx.sdlxliff')
    sxlf = Sdlxliff.load(file)
    xdoc = sxlf.to_json()

    assert xdoc['source_file'] == file
    assert len(xdoc['files']) == 2

    xfile0 = xdoc['files'][0]
    assert xfile0['srclang'] == 'ja-JP'
    assert xfile0['tgtlang'] == 'en-us'
    assert xfile0['properties']['original'] == 'test1.docx'
    assert xfile0['properties']['datatype'] == 'x-sdlfilterframework2'
    assert len(xfile0['groups']) == 2

    xgroup0 = xfile0['groups'][0]
    assert xgroup0['id'] == 'efa5d8d5-8291-48af-a47e-9cbd25e709e6'
    assert xgroup0['name'] == 'trans-unit'
    assert xgroup0['units'] == [{'id': '1',
                                'source': 'ビデオを使うと、伝えたい内容を明確に表現できます。',
                                 'target': '<mrk mtype="x-sdl-comment" sdl:cid="229d3377-d1c8-4419-a506-4f7ad7bf9d60"><mrk mtype="x-sdl-comment" sdl:cid="7990a264-9bb4-4c5e-8906-8d234f8497d8"><mrk mtype="x-sdl-comment" '
                                          'sdl:cid="e5011b5a-1970-473b-b94d-303dbad8058b">With videos</mrk>, you can clearly articulate</mrk></mrk> what you want to convey.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                {'id': '2',
                                'source': '[オンライン ビデオ] をクリックすると、追加したいビデオを、それに応じた埋め込みコードの形式で貼り付けできるようになります。',
                                 'target': 'Clicking Online Video will allow you to paste the video you want to add in the corresponding embed code.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                {'id': '3',
                                'source': 'キーワードを入力して、文書に最適なビデオをオンラインで検索することもできます。',
                                 'target': '<mrk mtype="x-sdl-comment" sdl:cid="af6deea3-97c0-4e9f-bcf5-2bf1b3635695">You can also enter keywords to search online for the best video for your document.</mrk>',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                ]

    xgroup1 = xfile0['groups'][1]
    assert xgroup1['id'] == '17eb0b62-5a6a-4e71-9610-b1d9b0c98c9b'
    assert xgroup1['name'] == 'trans-unit'
    assert xgroup1['units'] == [{'id': '4 a',
                                 'source': 'Word に用意されているヘッダー、フッター、表紙、テキスト ボックス デザインを組み合わせると、プロのようなできばえの文書を作成できます。',
                                 'target': 'Combine the header, footer, cover, and text box designs provided with Word to create professional-looking documents.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                {'id': '4 b a',
                                 'source': 'たとえば、一致する表紙、ヘッダー、サイドバーを追加できます。',
                                 'target': 'For example, you can add matching covers, headers, and sidebars.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                {'id': '4 b b a',
                                 'source': '[挿入] をクリックしてから、それぞれのギャラリーで目的の要素を選んでください。',
                                 'target': 'Click Insert, then select the desired element in each gallery.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                {'id': '4 b b b',
                                 'source': 'テーマとスタイルを使って、文書全体の統一感を出すこともできます。',
                                 'target': 'You can also use themes and styles to create a sense of unity throughout the document.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                ]

    xfile1 = xdoc['files'][1]
    assert xfile1['srclang'] == 'ja-JP'
    assert xfile1['tgtlang'] == 'en-us'
    assert xfile1['properties']['original'] == 'test2.docx'
    assert xfile1['properties']['datatype'] == 'x-sdlfilterframework2'
    assert len(xfile1['groups']) == 2

    xgroup2 = xfile1['groups'][0]
    assert xgroup2['id'] == 'c70a0969-f44e-4873-a2bc-7c370dc8d495'
    assert xgroup2['name'] == 'trans-unit'
    assert xgroup2['units'] == [{'id': '16',
                                 'source': 'ビデオを使うと、伝えたい内容を明確に表現できます。',
                                 'target': 'With videos, you can clearly articulate what you want to convey.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                {'id': '17',
                                 'source': '[オンライン ビデオ] をクリックすると、追加したいビデオを、それに応じた埋め込みコードの形式で貼り付けできるようになります。',
                                 'target': 'Clicking Online Video will allow you to paste the video you want to add in the corresponding embed code.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                {'id': '18',
                                 'source': 'キーワードを入力して、文書に最適なビデオをオンラインで検索することもできます。',
                                 'target': 'You can also enter keywords to search online for the best video for your document.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                ]

    xgroup3 = xfile1['groups'][1]
    assert xgroup3['id'] == '540c90a5-5bd1-4eeb-ab1a-d0fde204f123'
    assert xgroup3['name'] == 'trans-unit'
    assert xgroup3['units'] == [{'id': '19',
                                 'source': 'Word に用意されているヘッダー、フッター、表紙、テキスト ボックス デザインを組み合わせると、プロのようなできばえの文書を作成できます。',
                                 'target': 'Combine the header, footer, cover, and text box designs provided with Word to create professional-looking documents.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                {'id': '20',
                                 'source': 'たとえば、一致する表紙、ヘッダー、サイドバーを追加できます。',
                                 'target': 'For example, you can add matching covers, headers, and sidebars.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                {'id': '21',
                                 'source': '[挿入] をクリックしてから、それぞれのギャラリーで目的の要素を選んでください。',
                                 'target': 'Click Insert, then select the desired element in each gallery.',
                                 'srclang': 'ja-JP',
                                 'tgtlang': 'en-us',
                                 'properties': None},
                                ]
