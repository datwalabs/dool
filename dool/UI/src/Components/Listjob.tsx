import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import listjob from "../Data/ListJob";
import { Job, User, Operator, Task } from "../Interface/IListjob";
import Header from "./Header/header";
import "../listjob.scss";

export default function Listjob() {
  const listJob: [Job] = listjob;
  const [Listjob, setListjob] = useState(listJob);

  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/ListView", { state: Listjob }); // Replace with your target path
  };

  return (
    <div className="listJob-Container">
      <Header />
      <div className="listjob-header">JOB INFORMATION</div>

      <div className="listjob-table-container">
        <div className="row table-head">
          <div className="col-2">Job Name</div>
          <div className="col-3">Status</div>
          <div className="col-2">Last Run</div>
          <div className="col-2">Next Run</div>
          <div className="col-3"> Action</div>
        </div>
      </div>

      <div className="listjob-table-body">
        <div className="table-list-container">
          {Listjob.map((job) => (
            <div className="row table-list" key={job.job_id}>
              {" "}
              {/* Assuming job_id is unique */}
              <div className="col-2" onClick={handleClick}>
                {job.job_name}
              </div>
              <div className="col-3 status-container">
                <div className="circle" style={{ backgroundColor: "green" }}>
                  {job.success_runs}
                </div>
                <div className="circle" style={{ backgroundColor: "red" }}>
                  {job.fail_runs}
                </div>
              </div>
              <div className="col-2">
                <div className="lastRuns">{job.last_run}</div>
              </div>
              <div className="col-2">
                <div className="nextRuns">{job.next_run}</div>
              </div>
              <div className="col-3 action-buttons">
                <button>Run</button>
                <button>Edit</button>
                <button>Delete</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
