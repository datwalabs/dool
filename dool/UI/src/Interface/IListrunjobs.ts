export interface JobRun {
  run_id: number;
  status: string;
  started_at: string; // You could use Date if you plan to convert this string to a Date object
  finished_at: string; // Same as above
  logfile: string;
  logfile_id: number;
}