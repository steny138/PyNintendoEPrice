import os
import json
import math


class PreferNamingGenerator:

    def __init__(self, base_path) -> None:

        self.base_path = base_path

        # load jsons
        with open(f'{base_path}/lyc_chinese_characters.json', "r") as f:
            self.characters_arr = json.load(f)
        with open(f'{base_path}/eightyone.json', "r") as f:
            self.eightyone_arr = json.load(f)
        with open(f'{base_path}/sancai.json', "r") as f:
            self.sancai_dict = json.load(f)

    def gen(self, last_name, curr_zodiac) -> list:
        """產生匹配姓名"""

        score_dict = {}
        for second in self.characters_arr:
            for third in self.characters_arr:

                second_name = second["chars"][0]
                third_name = third["chars"][0]
                last_strokes = self.strokes(last_name)
                second_strokes = second["draw"]
                third_strokes = third["draw"]

                if second_strokes < 5 or third_strokes < 5 \
                        or second_strokes > 20 or third_strokes > 20:
                    continue

                # 先天命數 = 姓 + 名第一個字筆畫，尾數不為9,0

                if (last_strokes + second_strokes) % 10 in [9, 0]:
                    continue

                if (last_strokes + second_strokes + third_strokes) % 10 \
                        in [9, 0]:
                    continue

                sc = self.score(last_name, second_name, third_name)

                second_better, second_worse = self.zodiac(
                    curr_zodiac, second_strokes)
                third_better, third_worse = self.zodiac(
                    curr_zodiac, third_strokes)

                second_names = [c for c in second["chars"]
                                if c not in second_worse]

                third_names = [c for c in third["chars"]
                               if c not in third_worse]

                for name in [f'{last_name}{sec}{thd}'
                             for thd in third_names
                             for sec in second_names]:

                    if name[1] not in second_better and \
                            name[2] not in third_better:
                        continue

                    score_dict.setdefault(sc, []).append(name)

        with open(os.path.join(self.base_path, 'liu_name_new.json'), 'w') as f:
            json.dump(score_dict[100], f, ensure_ascii=False)

    def score(self, last_name, second_name, third_name):
        """計算姓名評分"""
        last_strokes = self.strokes(last_name)
        second_strokes = self.strokes(second_name)
        third_strokes = self.strokes(third_name)

        five_elements = self.calculate_five_elements(
            last_strokes, second_strokes, third_strokes)

        sancai_chr = "".join((five_elements['sky_attr'],
                              five_elements['people_attr'],
                              five_elements['land_attr']))

        sancai = self._sancai(sancai_chr)

        # 81
        score = self._81math(five_elements['sky'])['value']
        score += self._81math(five_elements['people'])['value']
        score += self._81math(five_elements['land'])['value']
        score += self._81math(five_elements['out'])['value']
        score += self._81math(five_elements['total'])['value']
        total_score = math.floor(score * 2 * 0.9) + sancai["value"]

        print(f"姓名評分: {last_name}{second_name}{third_name}")
        print("五格")
        print(f"天: {five_elements['sky_attr']}" +
              f"\n地: {five_elements['land_attr']}" +
              f"\n人: {five_elements['land_attr']}" +
              f"\n外: {five_elements['out_attr']}" +
              f"\n總: {five_elements['total_attr']}")
        print("三才")
        print(f"三才: {sancai_chr}" +
              f"\n評價: {sancai['text']}" +
              f"\n解釋: {sancai['content']}")
        print(f"81數: {score}")
        print(f"總評分: {total_score}")

        return total_score

    def info(self, last_name, second_name, third_name):
        """計算姓名評分詳情"""
        last_strokes = self.strokes(last_name)
        second_strokes = self.strokes(second_name)
        third_strokes = self.strokes(third_name)

        five_elements = self.calculate_five_elements(
            last_strokes, second_strokes, third_strokes)

        sancai_chr = "".join((five_elements['sky_attr'],
                              five_elements['people_attr'],
                              five_elements['land_attr']))

        sancai = self._sancai(sancai_chr)

        # 81
        score = self._81math(five_elements['sky'])['value']
        score += self._81math(five_elements['people'])['value']
        score += self._81math(five_elements['land'])['value']
        score += self._81math(five_elements['out'])['value']
        score += self._81math(five_elements['total'])['value']

        total_score = math.floor(score * 2 * 0.9) + sancai["value"]

        return {
            "five_elements": five_elements,
            "sancai_chr": sancai_chr,
            "sancai": sancai,
            "score_81": score,
            "total_score": total_score,
        }

    def calculate_five_elements(self,
                                last_name_strokes,
                                second_strokes,
                                third_strokes):
        """計算五格

        Args:
            last_name_strokes ([int]): 姓氏筆劃
            second_strokes ([int]): 名字第一個字筆劃
            third_strokes ([int]): 名字第二個字筆劃
        """
        # 天
        sky = last_name_strokes + 1
        # 地
        land = second_strokes + third_strokes
        # 人
        people = last_name_strokes + second_strokes
        # 外
        out_ = third_strokes + 1
        # 總
        total = last_name_strokes + second_strokes + third_strokes

        return {
            'sky': sky,
            'people': people,
            'land': land,
            'out': out_,
            'total': total,

            'sky_attr': self.attribute_num(sky),
            'people_attr': self.attribute_num(people),
            'land_attr': self.attribute_num(land),
            'out_attr': self.attribute_num(out_),
            'total_attr': self.attribute_num(total),
        }

    def _sancai(self, sancai_chr):
        """三才"""
        return self.sancai_dict[sancai_chr]

    def _81math(self, strokes):
        """對應 81數理"""
        return [i for i in self.eightyone_arr if i["draw"] == strokes][0]

    def zodiac(self, curr_zodiac, strokes):
        """十二生肖對應吉凶"""
        zodiac = self.__find_zodiac_dict(curr_zodiac)

        if not zodiac:
            return [], []

        return zodiac['better'].get(f'_{strokes}', []), \
            zodiac['worse'].get(f'_{strokes}', [])

    def __find_zodiac_dict(self, curr_zodiac):
        for file in os.listdir(self.base_path):
            if file.endswith(".json") and curr_zodiac in file:
                with open(os.path.join(self.base_path, file), "r") as f:
                    return json.load(f)

    def strokes(self, chr):
        """字的筆劃"""

        return self.__find_chr(chr).get('draw', None)

    def attribute(self, chr):
        """轉換五行

        １、２屬木，３、４屬火，５、６屬土，７、８屬金，９、０屬水
        """
        return self.__find_chr(chr).get('fiveEle', None)

    def attribute_num(self, num):
        """轉換五行

        １、２屬木，３、４屬火，５、６屬土，７、８屬金，９、０屬水
        """
        n = num % 10

        if n == 1 or n == 2:
            return "木"
        elif n == 3 or n == 4:
            return "火"
        elif n == 5 or n == 6:
            return "土"
        elif n == 7 or n == 8:
            return "金"
        elif n == 9 or n == 0:
            return "水"

        return ""

    def __find_chr(self, chr):
        for chr_strokes in [c for c in self.characters_arr]:
            if chr in chr_strokes['chars']:
                return chr_strokes

        return {}


if __name__ == "__main__":

    generator = PreferNamingGenerator("../static/naming")

    # generator.gen("劉", "tiger")

    # print(generator.score("劉", "恆", "宇"))

    name = "劉騏睿"
    generator.score(*name)
