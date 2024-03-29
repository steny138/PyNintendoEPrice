from flask import current_app as app
from .bot.line import LYCLineBot
from .baby.hosipital_state import BobsonClinicProgress
from flask import Blueprint
from .cache import get_distribute_cache, replace_clinic_cache
from .events.clinic import ClinicEvent

clinic_api_blueprint = Blueprint('clinic_api', __name__)

doctors = ['鄭偉吉', '孫正謙', '呂泓逸', '侯廣瓊', '李俊儀']


@clinic_api_blueprint.route('/api/v1/clinic/register_job',
                            methods=['GET', 'POST'])
def register_job():
    app.logger.info('clinic job had been called.')

    distribute_cache = get_distribute_cache()
    register_clinic_jobs = distribute_cache.get_many(
        *[f'clinic:{doctor}' for doctor in doctors])
    register_clinic_jobs = list(
        filter(lambda x: x is not None, register_clinic_jobs))

    if not register_clinic_jobs:
        return "NO Jobs"

    clinic = BobsonClinicProgress()
    event = ClinicEvent()
    bot_service = LYCLineBot(
        app.config['LINEBOT_CHANNEL_ACCESS_TOKEN'],
        app.config['LINEBOT_CHANNEL_SECRET'])

    clinic_progress_list = clinic.get_all_clinic_progress()

    for clinic_progress in clinic_progress_list:    # progressing clinics
        for clinic_jobs in register_clinic_jobs:    # every doctor list
            for clinic_job in clinic_jobs:          # every patient per doctor
                if not clinic_job.get("working", True):
                    continue
                if clinic_job['doctor'] != clinic_progress['doctor']:
                    continue
                if int(clinic_job.get("current", 0)) == \
                        int(clinic_progress.get("current", 0)):
                    continue

                msg = event.occurs(
                    [clinic_job['doctor'],
                     '門診',
                     f"{clinic_job['number']}"])

                if not msg:
                    continue

                # message not None
                bot_service.send_message(msg, clinic_job['user'])

                clinic_job['current'] = clinic_progress["current"]

                if "過號了" in msg:
                    # clean job in cache
                    clinic_job["working"] = False

    for clinic_jobs in register_clinic_jobs:    # every doctor list
        replace_clinic_cache(clinic_jobs[0]["doctor"], clinic_jobs)

    return 'OK'
