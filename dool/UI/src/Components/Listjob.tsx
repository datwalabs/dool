import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import listjob from "../Data/ListJob";
import { Job, User, Operator, Task } from "../Interface/IListjob";
import Header from "./Header/header";

import "../listjob.scss";

export default function Listjob() {
  const listJob: [Job] = listjob;
  const [Listjob, setListjob] = useState(listJob);
  const [show , setShow] = useState(false);
  const [jobObject, setjobObject] = useState([]);
  const [jobName, setJobName] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [cronExpression, setCronExpression] = useState('');

  // State to store the array of job objects
  const [jobList, setJobList] = useState<{ name: string; description: string; cron: string }[]>([]);


  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/ListView", { state: Listjob }); // Replace with your target path
  };

  const openModal = () => {
    setShow(!show);
  }

  // Function to handle the "Next" button click
  function handleNext() {
    const newJob = {
      name: jobName,
      description: jobDescription,
      cron: cronExpression,
    };

    // Add the new job to the jobList
    setJobList((prevList) => {
      const updatedList = [...prevList, newJob]; // Create a new list with the new job
      navigate("/Integration", { state: updatedList[0] }); // Pass the updated list
      return updatedList; // Return the updated list to update the state
    });

    // Reset input fields after adding the job
    setJobName('');
    setJobDescription('');
    setCronExpression('');
}



  return (
    <div className="listJob-Container">
      <Header />
      <div className="listjob-header">JOB INFORMATION</div>     

      <div className="listjob-table-container">
        <div className="createJob">
          <button onClick={() =>{
            openModal();
          }}>Create</button>
        </div>
        <div className="modal" style={{ display: show ? 'block' : 'none' }}>
        <div className="input-container">
          <input
            type="text"
            placeholder="Job Name"
            value={jobName}
            onChange={(e) => setJobName(e.target.value)}
          />
          <input
            type="text"
            placeholder="Job Description"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
          <input
            type="text"
            placeholder="Cron Expression"
            value={cronExpression}
            onChange={(e) => setCronExpression(e.target.value)}
          />
        </div>
        <button onClick={handleNext}>Next</button>
      </div>
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
                <button onClick={()=>{
                  navigate("/Integration",{ state: job }); // Replace with your target path
                }}>Run</button>
                <button onClick={()=>{
                  navigate("/EditIntegration", { state: job }); // Replace with your target path
                }}>Edit</button>
                <button>Delete</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
