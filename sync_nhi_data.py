import logging
from DataMaintenance.fetch_medical_site import FetchMedicalSites

logging.basicConfig(encoding='utf-8', level=logging.INFO)


def run_sync():
    runner = FetchMedicalSites()
    runner.update_all()


if __name__ == '__main__':
    run_sync()
