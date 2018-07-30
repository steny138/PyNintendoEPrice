import requests
from auth import Auth

domain = "https://ptx.transportdata.tw/MOTC/v2/Rail/THSR/"
default_limit_count = 20

auth = Auth()

def get_station():
    """GET /v2/Rail/THSR/Station 取得車站基本資料
    
    Returns:
        [dict] -- 車站基本資料
    """

    action = "Station"
    url = domain + action + '?a=' + __get_odata_parameter()

    headers = {}
    headers.update(auth.get_auth_header())

    r = requests.get(url, headers=headers)

    if r.status_code == requests.codes.ok:
        return r.json()

    return {}

def get_fare(departure, destination):
    """GET /v2/Rail/THSR/ODFare/{OriginStationID}/to/{DestinationStationID}
    取得指定[起訖站間]之票價資料
    
    Arguments:
        departure {str} -- 出發車站id
        destination {str} -- 到達車站id
    """
    if not departure:
        return {}
    if not destination:
        return {}

    action = "ODFare/{}/to/{}".format(departure, destination)

    url = domain + action + '?a=' + __get_odata_parameter()

    headers = {}
    headers.update(auth.get_auth_header())

    r = requests.get(url, headers=headers)

    if r.status_code == requests.codes.ok:
        return r.json()

    return {}

def get_timetable(no=''):
    """GET /v2/Rail/THSR/GeneralTimetable
    取得所有車次的定期時刻表資料
    
    Arguments:
        no {str} -- 指定車次
    """

    action = "GeneralTimetable"
    if no:
        action += "/TrainNo/{}".format(no)

    url = domain + action + '?a=' + __get_odata_parameter()

    headers = {}
    headers.update(auth.get_auth_header())

    r = requests.get(url, headers=headers)

    if r.status_code == requests.codes.ok:
        return r.json()

    return {}
    
def get_seat(id):
    """GET /v2/Rail/THSR/AvailableSeatStatusList/{StationID}
    取得動態指定[車站]的對號座剩餘座位資訊看板資料

    """

    if not id:
        return {}
    
    action = "AvailableSeatStatusList/{}".format(id)
    url = domain + action + '?a=' + __get_odata_parameter()

    headers = {}
    headers.update(auth.get_auth_header())

    r = requests.get(url, headers=headers)

    if r.status_code == requests.codes.ok:
        return r.json()

    return {}
    
def get_news():
    """GET /v2/Rail/THSR/News
    取得高鐵最新消息資料
    """

    action = "News"

    url = domain + action + '?a=' + __get_odata_parameter()

    headers = {}
    headers.update(auth.get_auth_header())

    r = requests.get(url, headers=headers)

    if r.status_code == requests.codes.ok:
        return r.json()

    return {}

def get_alert():
    """GET /v2/Rail/THSR/AlertInfo
    取得即時通阻事件資料

    """
    action = "AlertInfo"

    url = domain + action + '?a=' + __get_odata_parameter()

    headers = {}
    headers.update(auth.get_auth_header())

    r = requests.get(url, headers=headers)

    if r.status_code == requests.codes.ok:
        return r.json()

    return {}

def __get_odata_parameter(top =0, skip = 0 , format="", orderby="", filter=""):
    """統一整理odata的固定參數指定回傳
    
    Keyword Arguments:
        top {int} -- 回傳幾筆 (default: {0})
        skip {int} -- 跳過前面幾筆 (default: {0})
        format {str} -- 回傳格式 json or xml (default: {""})
        orderby {str} -- 排列順序, 傳入response欄位名稱 (default: {""})
        filter {str} -- 篩選條件 (default: {""})
    
    Returns:
        [type] -- odata parameter的querystring
    """
    param = {'top': top, 'skip': skip, 'orderby': orderby, 'format': format, 'filter': filter}

    result = ""
    if top > 0:
        result += "&$top={top}"
    if skip > 0:
        result += "&$skip={skip}"
    if orderby:
        result += "&$orderby={orderby}"
    if format:
        result += "&$format={format}"
    if filter:
        result += "&$filter={filter}"
    
    return result.format(**param)

if __name__ == '__main__':
    # print(get_station())
    # print(get_alert())
    # print(get_news())
    # print(get_fare('1000','1070'))
    # print(get_fare('1070','1000'))
    # print(get_timetable())
    # print(get_timetable('0681'))
    pass