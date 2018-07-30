import requests
from auth import Auth

domain = "https://ptx.transportdata.tw/MOTC/v2/Bus/"
default_limit_count = 20

auth = Auth()

def get_route(route_name=''):
    """GET /v2/Bus/Route/InterCity
    取得公路客運路線資料
    
    Returns:
        [dict] -- 車站基本資料
    """

    action = "Route/InterCity"
    if route_name:
        action += "/{}".format(route_name)
    
    url = domain + action + '?a=' + __get_odata_parameter()

    headers = {}
    headers.update(auth.get_auth_header())
    r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.ok:
        return r.json()

    return {}

def get_route_stop(route_name):
    """GET /v2/Bus/StopOfRoute/InterCity/{RouteName}
    取得指定[路線名稱]的公路客運路線與站牌資料

    路線資料會有 去+回+不同營運公司的排列組合列表
    Ex:
    1.國光客運 台北到台中
    2.國光客運 台中到台北
    3.統聯客運 台北到台中
    4.統聯客運 台中到台北
    """
    
    action = "StopOfRoute/InterCity"
    if route_name:
        action += "/{}".format(route_name)

    url = domain + action + '?a=' + __get_odata_parameter(top=500)

    headers = {}
    headers.update(auth.get_auth_header())
    r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.ok:
        return r.json()

    return {}
    pass

def get_operator_info():
    """GET /v2/Bus/Operator/InterCity
    取得公路客運的營運業者資料
    
    Returns:
        [dict] -- 車站基本資料
    """

    action = "Operator/InterCity"
    url = domain + action + '?a=' + __get_odata_parameter(top=500)

    headers = {}
    headers.update(auth.get_auth_header())
    r = requests.get(url, headers=headers)
    if r.status_code == requests.codes.ok:
        return r.json()

    return {}

def get_operator():
    """取得公路客運的營運業者資料 - 簡易版
    """
    
    operator = get_operator_info()
    if not operator:
        return operator
    
    return [{'name':x['OperatorName']['Zh_tw'], \
            'id': x['OperatorID'], \
            'code': x['OperatorCode'], \
            'no': x['OperatorNo'], \
            'provider_id': x['ProviderID'] } for x in operator]
    
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
    # print(get_route())
    # operator = get_operator_info()
    # for o in operator:
    #     print(o['OperatorName']['Zh_tw'])
    # print(get_operator())
    print(get_route_stop('9102'))