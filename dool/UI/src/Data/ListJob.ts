import { Job } from "../Interface/IListjob";

const listJob:[Job] = [{
    "job_id": 12,
    "job_name": "UDM",
    "cron": "8 * * * *",
    "is_active": true,
    "environment": 1,
    "created_by": {
      "user_id": 12,
      "username": "paresh.sahoo"
    },
    "next_run": "2024-09-21T12:23:34",
    "created_at": "2024-09-21T12:23:34",
    "last_run": "2024-09-21T12:23:34",
    "success_runs": 12,
    "fail_runs": 4,
    "failed_last_10": 2,
    "running_now": true,
    "tasks": [
      {
        "task_name": "calculate_wh",
        "operator": {
          "operator_name": "python3",
          "operator_slug": "python3",
          "operator_id": 3
        },
        "sequence": 2,
        "task_params": "main.py --model CALCULATW_WH"
      },
      {
        "task_name": "calculate_wh",
        "operator": {
          "operator_name": "python3",
          "operator_slug": "python3",
          "operator_id": 3
        },
        "sequence": 1,
        "task_params": "main.py --model DECALC"
      }
    ]
  }]

  export default listJob;