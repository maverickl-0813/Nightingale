import logging

from DataMaintenance.fetch_medical_site import FetchMedicalSites

logging.basicConfig(encoding='utf-8', level=logging.INFO)

if __name__ == '__main__':

    runner = FetchMedicalSites()
    # runner.update_all()
    runner.update_medical_centers()
    runner.update_regional_hospital()
    runner.update_district_hospital()
    runner.update_small_clinic()
    # runner.update_pharmacy()
