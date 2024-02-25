import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
from requests import RequestException

from core.models import Questionnaire


def send_file_to(filename: str, file: InMemoryUploadedFile, url: str, body: dict) -> bool:
    try:
        files = {filename: file}
        response = requests.post(url, files=files, data=body)
        if response.status_code == 200:
            return True
        return False
    except RequestException:
        return False


def get_all_questionnaire_by_patient(patient):
    return Questionnaire.objects.filter(fio=patient.fio, dob=patient.dob)
