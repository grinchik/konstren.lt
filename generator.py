import json

from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path

from typing import Dict
from typing import List
from typing import Optional
from typing import Literal

def file_content(file_path: str) -> str:
    return Path(file_path).read_text(encoding='utf-8')

Title = str
Lang = str
Stylesheet = str

@dataclass
class Config:
    title: Title
    lang: Lang

Chapter = str
Article = str

CardType = Literal['TITLE', 'LAST', 'ARTICLE']

@dataclass
class Paragraph:
    chapter: Chapter
    article: Article
    lt: str
    ru: str

@dataclass
class Card:
    card_type: CardType
    chapter: Chapter
    article: Article
    lines: List[Dict[str, str]]

@dataclass
class ViewModel:
    stylesheet: Stylesheet
    title: Title
    lang: Lang
    cards: List[Card]

@dataclass
class Attrs:
    id: Optional[str] = None
    className: Optional[str] = None
    lang: Optional[Lang] = None

InputType = Literal['checkbox']

@dataclass
class InputAttrs(Attrs):
    type: InputType = 'checkbox'
    value: Optional[str] = None

@dataclass
class LabelAttrs(Attrs):
    htmlFor: Optional[str] = None

def grouped_by_chapter(paragraphs: List[Paragraph]):
    result: Dict[Chapter, List[Paragraph]] = defaultdict(list)
    for paragraph in paragraphs:
        result[paragraph.chapter].append(paragraph)
    return result

def grouped_by_article(paragraphs: List[Paragraph]):
    result: Dict[Article, List[Paragraph]] = defaultdict(list)
    for paragraph in paragraphs:
        result[paragraph.article].append(paragraph)
    return result

def html(attrs: Attrs, children: List[str]):
    NEW_LINE='\n'
    return f'<!DOCTYPE html>\n<html lang="{attrs.lang}">\n{NEW_LINE.join(children)}\n</html>'

def head(children: List[str]):
    NEW_LINE='\n'
    return f'<head>\n<meta charset="utf-8" />\n<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />\n{NEW_LINE.join(children)}\n</head>'

def title(title: str):
    return f'<title>{title}</title>'

def body(children: List[str]):
    NEW_LINE='\n'
    return f'<body>\n{NEW_LINE.join(children)}\n</body>'

def p(children: List[str]):
    NEW_LINE='\n'
    return f'<p>\n{NEW_LINE.join(children)}\n</p>'

def h1(attrs: Attrs, header: str):
    id = f' id="{attrs.id}"' if attrs.id is not None else ''
    className = f' class="{attrs.className}"' if attrs.className is not None else ''

    return f'<h1{id}{className}>{header}</h1>'

def h2(attrs: Attrs, header: str):
    id = f' id="{attrs.id}"' if attrs.id is not None else ''
    className = f' class="{attrs.className}"' if attrs.className is not None else ''

    return f'<h2{id}{className}>{header}</h2>'

def h3(attrs: Attrs, header: str):
    id = f' id="{attrs.id}"' if attrs.id is not None else ''
    className = f' class="{attrs.className}"' if attrs.className is not None else ''

    return f'<h3{id}{className}>{header}</h3>'

def div(attrs: Attrs, children: List[str]):
    NEW_LINE='\n'

    id = f' id="{attrs.id}"' if attrs.id is not None else ''
    className = f' class="{attrs.className}"' if attrs.className is not None else ''

    return f'<div{id}{className}>\n{NEW_LINE.join(children)}\n</div>'

def span(attrs: Attrs, children: List[str]):
    NEW_LINE='\n'

    id = f' id="{attrs.id}"' if attrs.id is not None else ''
    className = f' class="{attrs.className}"' if attrs.className is not None else ''
    lang = f' lang="{attrs.lang}"' if attrs.lang is not None else ''

    return f'<span{id}{className}{lang}>\n{NEW_LINE.join(children)}\n</span>'

def style(stylesheet: Stylesheet):
    return f'<style>\n{stylesheet}\n</style>'

def input(inputAttrs: InputAttrs):
    id = f' id="{inputAttrs.id}"' if inputAttrs.id is not None else ''
    className = f' class="{inputAttrs.className}"' if inputAttrs.className is not None else ''
    type = f' type="{inputAttrs.type}"'
    value = f' value="{inputAttrs.value}"' if inputAttrs.value is not None else ''

    return f'<input{id}{className}{type}{value} />'

def label(labelAttrs: LabelAttrs, children: List[str]):
    NEW_LINE='\n'

    id = f' id="{labelAttrs.id}"' if labelAttrs.id is not None else ''
    className = f' class="{labelAttrs.className}"' if labelAttrs.className is not None else ''
    htmlFor = f' for="{labelAttrs.htmlFor}"' if labelAttrs.htmlFor is not None else ''

    return f'<label{id}{className}{htmlFor}>\n{NEW_LINE.join(children)}\n</label>'

def a(attrs: Attrs, href: str, text: str):
    className = f' class="{attrs.className}"' if attrs.className is not None else ''
    return f'<a href="{href}"{className}>{text}</a>'

def view_model(
        config: Config,
        stylesheet: Stylesheet,
        paragraphs: List[Paragraph],
) -> ViewModel:
    cards: List[Card] = []

    for index, (chapter, chapter_paragraphs) in enumerate(grouped_by_chapter(paragraphs).items()):
        for article, article_paragraphs in grouped_by_article(chapter_paragraphs).items():
            lines: List[Dict[str, str]] = []
            for paragraph in article_paragraphs:
                lines.append({
                    'lt': paragraph.lt,
                    'ru': paragraph.ru,
                })

            card_type: CardType = 'TITLE' if index == 0 else 'ARTICLE'

            cards.append(
                Card(
                    card_type=card_type,
                    chapter=chapter,
                    article=article,
                    lines=lines,
                )
            )

    cards.append(
        Card(
            card_type='LAST',
            chapter='',
            article='',
            lines=[],
        )
    )

    return ViewModel(
        stylesheet=stylesheet,
        title=config.title,
        lang=config.lang,
        cards=cards,
    )

def translate_toggle_id(lineIdx: int, cardIdx: int) -> str:
    return '_'.join(['tr', str(lineIdx), str(cardIdx)])

def CardView(cardIdx: int, card: Card):
    if card.card_type == 'LAST':
        return div(
            Attrs(id=str(cardIdx), className='card title-card references-card'),
                [
                    div(Attrs(className='references-section'), [
                        h2(Attrs(className='references-title'), 'Šaltiniai'),
                        div(Attrs(className='references-list'), [
                            p([
                                a(
                                    Attrs(),
                                    'https://www.lrs.lt/home/Konstitucija/Konstitucija.htm',
                                    'Lietuvos Respublikos Seimas (LT)',
                                ),
                            ]),
                            p([
                                a(
                                    Attrs(),
                                    'https://www.lrs.lt/home/Konstitucija/Constitution.htm',
                                    'Lietuvos Respublikos Seimas (EN)',
                                ),
                            ]),
                            p([
                                a(
                                    Attrs(),
                                    'https://www.lrs.lt/home/Konstitucija/Konstitucija_RU.htm',
                                    'Lietuvos Respublikos Seimas (RU)',
                                ),
                            ]),
                            p([
                                a(
                                    Attrs(),
                                    'https://www.e-tar.lt/portal/en/legalAct/TAR.47BB952431DA/asr',
                                    'Teisės Aktų Registras (LT)',
                                ),
                            ]),
                        ]),
                    ]),
                    div(Attrs(className='credits-section'), [
                        p([
                            a(
                                Attrs(),
                                'https://github.com/grinchik/konstren.lt',
                                'github.com/grinchik/konstren.lt',
                            ),
                        ]),
                    ]),
                ],
            )
    elif card.card_type == 'TITLE':
        return div(
            Attrs(id=str(cardIdx), className='card title-card'),
            [
                h1(Attrs(), card.chapter),
                div(Attrs(className='article-text'), [
                    p([
                        input(InputAttrs(
                            className='translate-toggle',
                            id=translate_toggle_id(lineIdx, cardIdx),
                            type='checkbox',
                        )),
                        label(LabelAttrs(
                            className='translatable' if line['ru'] != '' else '',
                            htmlFor=translate_toggle_id(lineIdx, cardIdx) if line['ru'] != '' else None,
                        ), [
                            span(Attrs(lang='lt'), [ line['lt'] ]),
                            span(Attrs(lang='ru'), [ line['ru'] ]),
                        ])
                    ] if line['ru'] != '' else [
                        line['lt']
                    ])
                    for lineIdx, line in enumerate(card.lines)
                ]),
            ],
        )
    else: # ARTICLE
        return div(
            Attrs(id=str(cardIdx), className='card'),
            [
                h2(Attrs(className='chapter-title'), card.chapter),
                h3(Attrs(className='article-number'), card.article),
                div(Attrs(className='article-text'), [
                    p([
                        input(InputAttrs(
                            className='translate-toggle',
                            id=translate_toggle_id(lineIdx, cardIdx),
                            type='checkbox',
                        )),
                        label(LabelAttrs(
                            className='translatable' if line['ru'] else '',
                            htmlFor=translate_toggle_id(lineIdx, cardIdx) if line['ru'] else None,
                        ), [
                            span(Attrs(lang='lt'), [ line['lt'] ]),
                            span(Attrs(lang='ru'), [ line['ru'] ]),
                        ])
                    ] if line['ru'] else [
                        line['lt']
                    ])
                    for lineIdx, line in enumerate(card.lines)
                ]),
            ],
        )

def view(view_model: ViewModel) -> str:
    return html(Attrs(lang='lt'), [
        head([
            title(view_model.title),
            style(view_model.stylesheet),
        ]),
        body([
            div(Attrs(className='container'), [
                CardView(cardIdx, card)
                for cardIdx, card in enumerate(view_model.cards)
            ]),
        ]),
    ])

if __name__ == '__main__':
    stylesheet = file_content('stylesheet.css')

    paragraphs_raw = file_content('source/paragraphs.json')
    paragraphs =  [
        Paragraph(**{k: v for k, v in item.items() if k != "_"})
        for item in json.loads(paragraphs_raw)
    ]

    config = Config(
        title = 'Lietuvos Respublikos Konstitucija',
        lang='lt',
    )

    print(view(view_model(config, stylesheet, paragraphs)))
