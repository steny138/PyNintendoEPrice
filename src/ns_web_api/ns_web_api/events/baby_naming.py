import logging
from ..events.default import DefaultEvent
from ..naming.naming import PreferNamingGenerator

logger = logging.getLogger('flask.app')


class BabyNamingEvent(DefaultEvent):
    """ 小孩命名事件
    """

    def __init__(self):
        super().__init__()

    def occurs(self, vocabulary, *args, **kwargs):
        """小孩命名事件觸發
        """

        if not vocabulary:
            return

        logger.info(vocabulary)
        name = "".join(vocabulary)
        if "劉" in name[:1] and len(name) == 3:
            return self.__baby_naming_event(name)

        return

    def __baby_naming_event(self, name):
        """小孩事件處理

        Arguments:
            name {list of string} -- request name

        Returns:
            [string] -- reply message
        """
        generator = PreferNamingGenerator("ns_web_api/static/naming")

        info = generator.info(*name)
        five_elements = info["five_elements"]
        sancai_chr = info["sancai_chr"]
        sancai = info["sancai"]
        score = info["score_81"]
        total_score = info["total_score"]

        reply_message = ''

        reply_message = f"姓名評分: {name}"
        reply_message += "\n五格"
        reply_message += f" 天: {five_elements['sky_attr']}"
        reply_message += f" 地: {five_elements['land_attr']}"
        reply_message += f" 人: {five_elements['land_attr']}"
        reply_message += f" 外: {five_elements['out_attr']}"
        reply_message += f" 總: {five_elements['total_attr']}"

        reply_message += f"\n三才: {sancai_chr}"
        reply_message += f"\n三才評價: {sancai['text']}"
        reply_message += f"\n三才解釋: {sancai['content']}"

        reply_message += f"\n81數: {score}"
        reply_message += f"\n總評分: {total_score}"

        return reply_message
