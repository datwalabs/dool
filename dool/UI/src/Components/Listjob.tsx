import React, { useState } from "react";
import listjob from "../Data/ListJob";
import { Job, User, Operator, Task } from "../Interface/IListjob";
import Header from "./Header/header";
import "../listjob.scss";

export default function Listjob() {
  const listJob: [Job] = listjob;
  const [Listjob, setListjob] = useState(listJob);
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
        <div className="row table-list">
          <div className="col-2">{Listjob[0].job_name}</div>
          <div className="col-3 status-container">
            <div className="circle" style={{backgroundColor:"green"}}>{Listjob[0].success_runs}</div>
            <div className="circle" style={{backgroundColor:"red"}}>{Listjob[0].fail_runs}</div>
            {/* <div className='circle'></div> */}
          </div>
          <div className="col-2">
            <div className="lastRuns">{Listjob[0].last_run}</div>
          </div>
          <div className="col-2">
            <div className="nextRuns">{Listjob[0].next_run}</div>
          </div>
          <div className="col-3 action-buttons">
            <button>
Run
            </button>
            <button>
                Edit
            </button>
            <button>
                Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
