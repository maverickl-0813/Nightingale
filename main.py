import logging

from fetch_medical_site import FetchMedicalSites

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

if __name__ == '__main__':

    runner = FetchMedicalSites()
    runner.update_all()
    # runner.update_pharmacy()
