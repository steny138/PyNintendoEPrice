import re
import cache
from events.default import DefaultEvent
from baby.hosipital_state import BobsonClinicProgress


class ClinicEvent(DefaultEvent):
    """ 門診事件
    """

    def __init__(self):
        super().__init__()

    def occurs(self, vocabulary, *args, **kwargs):
        """門診事件觸發
        """
        if not vocabulary:
            return

        if "門診" in vocabulary:
            self.logger.debug('occurs at ClinicEvent')

            return self.__clinic_event(vocabulary,
                                       kwargs.get('user_id', None))

        return

    def __clinic_event(self, vocabulary, user_id=None):
        clinic = BobsonClinicProgress()

        # xxx門診預約yyy號
        spilit_index = vocabulary.index("門診")
        doctor = ''.join(vocabulary[:spilit_index])
        number = ''.join(vocabulary[spilit_index+1:])
        number = re.search('\\d+', number).group(0)

        # get progress from bobson api
        r = clinic.check_clinic_progress(doctor)
        self.logger.info(f'line user: {user_id}')

        if r:
            # register job for check clinic status
            if user_id:
                reserve_info = {
                    'doctor': doctor,
                    'number': int(number),
                    'user': user_id
                }

                cache.append_clinic_cache(doctor, reserve_info)

                self.logger.info(f'register clinic job for {doctor}')

            current = int(r["current"])
            mine = int(number)
            diff = mine-current

            notice_message = f'還差{diff}個，請稍候'

            if diff > 100:
                return
            elif diff < 0:
                notice_message = '過號了'
            elif diff < 20:
                notice_message = f'剩下{diff}個了，趕快出門'

            return f'{doctor}[{r["current"]}號]{notice_message}，在{r["room"]}看診'

        return f'{doctor} 尚無門診'
