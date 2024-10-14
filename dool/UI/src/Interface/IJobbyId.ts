export interface Operator {
    operator_id: number;
    operator_name: string;
    operator_slug: string;
    description: string;
  }
  
  export interface Task {
    task_id: number;
    task_name: string;
    operator_id: number;
    sequence: number;
    task_param: string;
    operator: Operator;
  }
  
  export interface Job {
    job_id: number;
    job_name: string;
    cron_expression: string;
    is_active: number;
    environment: string;
    tasks: Task[];
  }
  