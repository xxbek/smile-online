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
        'fio': patient.fio,
        'birthday': patient.dob,
        'address': patient.slug,
        'mobile': patient.phone_number,
        'number_per': quest.name,
        'date': patient.added_at,
        'word_key': [keyword[0].name for keyword in patient.get_keywords_with_answers()]
    }
    return body


