import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def build_alert_msg(schedule = None):

    if not schedule:
        schedule = get_schedule()
    
    msg = ''

    today = datetime.today()
    today = datetime(today.year, today.month, today.day)
    print(schedule)
    if "presale_s" in schedule and "presale_d" in schedule:
        presale_s = datetime.strptime(schedule["presale_s"], "%m/%d")
        presale_d = datetime.strptime(schedule["presale_d"], "%m/%d")
        
        presale_s = presale_s.replace(year=today.year)
        presale_d = presale_d.replace(year=today.year)

        if presale_s <= today <= presale_d:
            msg += f'預購繳費就從 *{schedule["presale_s"]}* ~ *{schedule["presale_d"]}*'

    if "receive_s" in schedule and "receive_d" in schedule:
        receive_s = datetime.strptime(schedule["receive_s"], "%m/%d")
        receive_d = datetime.strptime(schedule["receive_d"], "%m/%d")

        receive_s = receive_s.replace(year=today.year)
        receive_d = receive_d.replace(year=today.year)

        if receive_s <= today <= receive_d:
            if receive_s == today:
                msg += f'*{schedule["receive_s"]}* ~ *{schedule["receive_d"]}* 就可到指定超商領取口罩囉'

            if receive_d == today:
                msg += f'今天是 *{schedule["receive_d"]}* 最後一天可到指定超商領取口罩別忘囉'

    if msg and "periods" in schedule:
        msg = f'第{schedule["periods"]}期口罩預購: \r\n{msg}'

    return msg

def get_schedule():
    url = "https://emask.taiwan.gov.tw/msk/index.jsp"
    user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    headers = {'User-Agent': user_agent}

    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        print(resp)

    soup = BeautifulSoup(resp.text, 'html.parser')

    schedule_contents = soup.select('div.row.justify-content-center > div.col > p')

    result = {}

    for schedule_content in schedule_contents:

        if not schedule_content:
            continue

        if not schedule_content.text:
            continue

        match_periods = re.search(r'(?<=第)\d+(?=期口罩預購各階段開放時程)', schedule_content.text)

        if match_periods:
            result['periods'] = match_periods.group()
            continue

        match_presale = re.search(r'(?<=\(新訂購\)預購繳費)\s?(?P<sd>\d+\/\d+)\s?(?P<st>\d+:\d+)\s?-\s?(?P<dd>\d+\/\d+)\s?(?P<dt>\d+:\d+)', schedule_content.text)

        if match_presale:
            result['presale_s'] = match_presale.group('sd')
            result['presale_d'] = match_presale.group('dd')
            continue

        match_receive = re.search(r'(?<=領取口罩)\s?(?P<sd>\d+\/\d+)\s?(?P<st>\d+:\d+)\s?-\s?(?P<dd>\d+\/\d+)\s?(?P<dt>\d+:\d+)', schedule_content.text)

        if match_receive:
            result['receive_s'] = match_receive.group('sd')
            result['receive_d'] = match_receive.group('dd')
            continue

    return result


if __name__ == "__main__":
    print(build_alert_msg())