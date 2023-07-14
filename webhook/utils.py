import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
from requests import RequestException

from core.models import Questionnaire, Quest


def send_file_to(file: InMemoryUploadedFile, url: str, body: dict) -> bool:
    try:
        files = {'file': file}
        response = requests.post(url, files=files, data=body)
        if response.status_code == 200:
            return True
        return False
    except RequestException:
        return False


def generate_body(patient: Questionnaire, quest: Quest) -> dict:
    body = {
        'fullname': patient.fio,
        'birthday': patient.dob,
        'phone': patient.phone_number,
        'questionnaire_type': quest.name,
        'questionnaire_creation_date': patient.added_at
    }
    return body


