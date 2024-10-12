// jobInterfaces.ts
export interface User {
    user_id: number;
    username: string;
}

export interface Operator {
    operator_name: string;
    operator_slug: string;
    operator_id: number;
}

export interface Task {
    task_name: string;
    operator: Operator;
    sequence: number;
    task_params: string;
}

export interface Job {
    job_id: number;
    job_name: string;
    cron: string;
    is_active: boolean;
    environment: number;
    created_by: User;
    next_run: string; // Consider using Date for type safety
    created_at: string; // Consider using Date for type safety
    last_run: string; // Consider using Date for type safety
    success_runs: number;
    fail_runs: number;
    failed_last_10: number;
    running_now: boolean;
    tasks: Task[];
}
