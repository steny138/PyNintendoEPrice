from typing import List


class RichMenuAction:
    label: str
    type: str
    text: str


class RichMenuBounds:
    x: int
    y: int
    width: int
    height: int


class RichMenuSize:
    width: int
    height: int


class RichMenuAlias:
    richMenuAliasId: str
    richMenuId: str


class RichMenuArea:
    bounds: RichMenuBounds
    action: RichMenuAction


class RichMenu:
    richMenuId: str
    name: str
    size: RichMenuSize
    chatBarText: str
    selected: bool
    areas: List[RichMenuArea]


# Request
class CreateRichMenu:
    isDefault: bool
    imgUrl: str
    richDetail: RichMenu

# Responses


class RichMenuAliasResponse:
    aliases: List[RichMenuAlias]


class RichMenuResponse:
    richmenus: List[RichMenu]
