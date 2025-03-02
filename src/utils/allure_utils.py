import json
import os

import allure
import pytest

from src.consts import ROOTDIR
from src.data.logs import MsgLog
from src.utils.logging_utils import logger


def log_step_to_allure():
    test_steps = []
    _msg_logs = MsgLog.step_logs

    # Find index step in list
    # get description from index
    steps_index = [
        index for index, value in enumerate(_msg_logs)
        if ("step" or "steps" or "Should see") in value.lower()
    ]

    for i in range(len(steps_index)):
        if i == (len(steps_index) - 1):
            test_steps.append(_msg_logs[steps_index[i]:])
            break
        test_steps.append(_msg_logs[steps_index[i]: steps_index[i + 1]])

    # Log test to allure reports
    for steps in test_steps:
        step = steps.pop(0)

        with allure.step(step):
            for verify in steps:
                with allure.step(verify):
                    pass

    del _msg_logs[:]


def custom_allure_report(allure_dir):
    allure_dir = ROOTDIR / allure_dir
    allure_result_files = [f for f in os.listdir(allure_dir) if f.endswith("result.json")]

    # sort result files based on created time
    files = [os.path.join(allure_dir, f) for f in allure_result_files]
    files.sort(key=lambda x: os.path.getmtime(x))

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                data["attachments"] = [item for item in data["attachments"] if item["name"] != "log"]

                cur_parent_suite = data["labels"][0]["value"]
                data["labels"][0]["value"] = " ".join(cur_parent_suite.split(".")[-1].split("_")).title()
                data["name"] = " ".join(data["labels"][1]["value"].split("_")).title()
                data["labels"].pop(1)

                if data["status"] == "failed":
                    data["steps"][-1]["steps"][-1]["status"] = "failed"

                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)  # Write with indentation for readability

        except Exception as e:
            logger.error(f"Error processing file {os.path.basename(file_path)}: {e}")


if __name__ == '__main__':
    custom_allure_report("allure-results1")
