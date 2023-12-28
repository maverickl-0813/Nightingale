import logging
import datetime
from pathlib import Path
from DataMaintenance.fetch_medical_site import FetchMedicalSites

logging.basicConfig(encoding='utf-8', level=logging.INFO)
# timestamp_file = 'sync.timestamp'


def run_sync():
    runner = FetchMedicalSites()
    # runner.update_all()
    runner.update_medical_centers()
    runner.update_regional_hospital()
    runner.update_district_hospital()
    runner.update_small_clinic()
    # runner.update_pharmacy()

    # Write timestamp to file.
    # with open(timestamp_file, 'w', encoding='utf-8') as f:
    #     f.write(f"{datetime.datetime.now()}")


if __name__ == '__main__':
    # timestamp = Path(timestamp_file)
    # if not timestamp:
    #     run_sync()
    run_sync()
