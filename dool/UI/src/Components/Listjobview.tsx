import React, { useState } from "react";
import Header from "./Header/header";
import "../listjob.scss";
import { useLocation } from "react-router-dom";
import { JobRun } from "../Interface/IListrunjobs";
import Runjobs from "../Data/JobRuns";

export default function Listjobview() {
  const location = useLocation();
  const Listjob = location.state; // Access the passed data here
  const [jobdata, setJobdata] = useState(Runjobs);
  return (
    <div>
      <Header />
      {Listjob ? (
        <div className="listjob-table-body">
          <div className="row table-list">
            <div className="col-2">{Listjob[0].job_name}</div>
            <div className="col-3 status-container">
              <div className="circle" style={{ backgroundColor: "green" }}>
                {Listjob[0].success_runs}
              </div>
              <div className="circle" style={{ backgroundColor: "red" }}>
                {Listjob[0].fail_runs}
              </div>
              {/* <div className='circle'></div> */}
            </div>
            <div className="col-2">
              <div className="lastRuns">{Listjob[0].last_run}</div>
            </div>
            <div className="col-2">
              <div className="nextRuns">{Listjob[0].next_run}</div>
            </div>
            <div className="col-3 action-buttons">
              <button>Run</button>
              <button>Edit</button>
              <button>Delete</button>
            </div>
          </div>
        </div>
      ) : (
        "No data"
      )}

      <div className="runJob-container">
        <div className="runjob-table">
          <div className="row m-0 runjob-table-headers">
            <div className="col"> RUN-ID</div>
            <div className="col">STATUS</div>
            <div className="col">START TIME</div>
            <div className="col">END TIME</div>
            <div className="col">LOGS</div>
          </div>
          <div className="runjob-table-body">
            {jobdata?.map((job) => (
              <div className="row m-0" key={job.run_id}>
                <div className="col">{job.run_id}</div>
                <div className="col">{job.status}</div>
                <div className="col">{job.started_at}</div>
                <div className="col">{job.finished_at}</div>
                <div className="col">{job.logfile}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
