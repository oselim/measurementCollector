from datetime import datetime
import json
import logging
from ripe.atlas.cousteau import MeasurementRequest, AtlasResultsRequest

logging.basicConfig(filename="data/measurement_collect.log", filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
measurement_filters = {
    "start_time__gte": datetime(2021, 1, 1),
    "stop_time__lte": datetime(2021, 1, 2),
    "type": "traceroute",
    "af": 4,
    "page_size": 500
}

measurements = MeasurementRequest(**measurement_filters)

measurement_ids = []
results_list = []

for msm in measurements:
    measurement_id = msm["id"]
    measurement_ids.append(measurement_id)
    is_success, results = AtlasResultsRequest(**{"msm_id": measurement_id}).create()
    logging.info("Result request is successful: %s", is_success)
    if is_success:
        results_list.extend(results)
        logging.info("Total measurements: %s, processed measurements: %s, Results size: %s, processed results: %s",
                     str(measurements.total_count), str(len(measurement_ids)), str(len(results)),
                     str(len(results_list)))

jsonString = json.dumps(results_list)
jsonFile = open("data/results_list-ipv4_traceroute-(21-1-1_21-1-2).json", "w")
jsonFile.write(jsonString)
jsonFile.close()

# open output file for writing
with open('data/measurement_ids.txt', 'w') as file_handle:
    json.dump(measurement_ids, file_handle)
file_handle.close()

logging.info("Measurements size: %s", str(measurements.total_count))
logging.info("Measurement IDs size: %s", str(len(measurement_ids)))
logging.info("Results size: %s", str(len(results_list)))
