import requests
from types import SimpleNamespace


class BobsonClinicProgress():
    """ find bobson clinic progress
    """

    def check_clinic_progress(self, doctor_name):
        clinics = self.__parse_clinic_progress(self.__get_clinic_progress())

        return next((clinic for clinic in clinics
                     if clinic['doctor'] == doctor_name and
                     clinic['status'] == '看診中'), None)

    def get_all_clinic_progress(self):
        clinics = self.__parse_clinic_progress(self.__get_clinic_progress())

        return [clinic for clinic in clinics
                if clinic['status'] == '看診中']

    def __parse_clinic_progress(self, clinic_progress):

        if clinic_progress.status != '1':
            return []

        for clinic in clinic_progress.data:
            # 醫生名字
            # 診間
            # 看診號碼
            # 看診狀況：看診中、準備中、休息

            yield {
                'doctor': clinic.doctor_name,
                'current': next(iter(clinic.wait_list)),
                'room': clinic.clinic_name,
                'status': clinic.clinic_status
            }

    def __get_clinic_progress(self):
        payload = {'vcode': 'o%2bs2SgZoJFQ='}

        r = requests.post(
            "https://fc3.bobson.biz/api/get-new-clinicdata", data=payload)

        if r.status_code == requests.codes.ok:

            return r.json(object_hook=lambda d: SimpleNamespace(**d))

        return {}


if __name__ == '__main__':
    clinic = BobsonClinicProgress()

    r = clinic.check_clinic_progress("呂泓逸")
    print(r)
