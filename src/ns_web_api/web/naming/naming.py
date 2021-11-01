import os
import json


class PreferNamingGenerator:

    def __init__(self, base_path) -> None:

        self.base_path = base_path

        # load jsons
        with open(f'{base_path}/chinese_characters.json', "r") as f:
            self.characters_arr = json.load(f)
        with open(f'{base_path}/eightyone.json', "r") as f:
            self.eightyone_arr = json.load(f)
        with open(f'{base_path}/sancai.json', "r") as f:
            self.sancai_dict = json.load(f)

    def gen(self, last_name, curr_zodiac) -> list:
        """產生匹配姓名"""

        pass

    def score(self, last_name, second_name, third_name) -> list:
        """計算姓名評分"""
        last_strokes = self.strokes(last_name)
        second_strokes = self.strokes(second_name)
        third_strokes = self.strokes(third_name)

        five_elements = self.calculate_five_elements(
            last_strokes, second_strokes, third_strokes)
        print(five_elements)

        sancai_chr = "".join((five_elements['sky_attr'],
                              five_elements['people_attr'],
                              five_elements['land_attr']))

        sancai = self._sancai(sancai_chr)
        print(sancai)

        # 81
        score = self._81math(five_elements['sky'])['value']
        print(score)
        score += self._81math(five_elements['people'])['value']
        print(score)
        score += self._81math(five_elements['land'])['value']
        print(score)
        score += self._81math(five_elements['out'])['value']
        print(score)
        score += self._81math(five_elements['total'])['value']
        print(score)
        print(f"81: {score}")

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
            'totla_attr': self.attribute_num(total),
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

    generator.score("劉", "倚", "汎")
