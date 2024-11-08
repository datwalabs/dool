import React, { useState } from "react";
import jobIntegrationData from "../Data/JobIntegration";
import Header from "./Header/header";
import "../listjob.scss";
import { useLocation } from "react-router-dom";
import { jobIntegration } from "../Interface/IJobIntegration";

export default function JobIntegration() {
  const [IntegrationData, setIntegrationData] = useState(jobIntegrationData);
  const [show, setShow] = useState(false);
  const [jobData, setJobdata] = useState<any>([]);
  const [taskName, setTaskName] = useState("");
  const [taskParams, settaskParams] = useState("");
  const [stepList, setSteplist] = useState<jobIntegration[][]>([]); // Array of arrays for grouping steps
  const [showListView, setShowListView] = useState(false); // Track if list-view-container is visible or hidden
  const [currentStepIndex, setCurrentStepIndex] = useState<{
    groupIndex: number | null;
    stepIndex: number | null;
    position: "below" | "right";
  }>({
    groupIndex: null,
    stepIndex: null,
    position: "below",
  }); // Keep track of the current step and group
  const [jobList, setJobList] = useState<{ name: string; params: string }[]>(
    []
  );

  const location = useLocation();
  const Listjob = location.state; // Access the passed data here
  console.log(Listjob[0]);

  // Create object and close the list view
  function createObject(data: any,updatedList:any) {
    const { groupIndex, stepIndex, position } = currentStepIndex;
    setSteplist((prevList) => {
      const newList = [...prevList];
       
      data['taskName'] = updatedList.name;
      data['taskParams'] = updatedList.params;

      if (groupIndex === null) {
        // Initial case: Add the first group and step
        return [[data]];
      } else {
        if (position === "below") {
          // Insert below the current step in the same group
          newList.splice(groupIndex + 1, 0, [data]);
        } else if (position === "right" && stepIndex !== null) {
          // Insert to the right within the same group
          newList[groupIndex] = [...newList[groupIndex]];
          newList[groupIndex].splice(stepIndex + 1, 0, data); // Insert at the next position in the group
        }
      }
      console.log(stepList)
      return newList;
    });

    setShowListView(false); // Close the list-view-container after adding a step
  }

  const openModal = () => {
    setShow(!show);
  };

  // Function to handle the "Next" button click
  function handleNext() {
    const newJob = {
      name: taskName,
      params: taskParams,
    };
    console.log("jobList",newJob);
    setShow(!show);
    // Add the new job to the jobList
    setJobList((prevList) => {
      const updatedList = [...prevList, newJob]; // Create a new list with the new job
      return updatedList; // Return the updated list to update the state
    });
    createObject(jobData,newJob);
   

    // Reset input fields after adding the job
    setTaskName("");
    settaskParams("");
  }

  // Function to merge jobList and stepList into the desired format
  function submitData() {
    const tasks: any = [];
      // Assuming stepList is structured as an array of arrays
      stepList.forEach((group, groupIndex) => {
        group.forEach((step, stepIndex) => {
          // Create the task object
          const task = {
            task_name: step.taskName,
            operator_id:  step.operator_id, // Adjust this based on your data structure
            sequence: groupIndex + 1, // Using the job's index as sequence
            task_params: step.taskParams,
          };
          tasks.push(task);
        });
      });

    // Create the final data structure
    const finalData = {
      tasks: tasks,
    };

    const createJobRequestBody = {
      "job_name": Listjob.name ,
      "cron": Listjob.cron,
      "is_active": true,
      "environment": 1,
      "tasks": tasks
    }


    console.log(createJobRequestBody);
  }

  // Toggle the visibility of the list-view-container and set the current step position
  function toggleListView(
    groupIndex: number | null = null,
    stepIndex: number | null = null,
    position: "below" | "right" = "below"
  ) {
    setCurrentStepIndex({ groupIndex, stepIndex, position }); // Set the current group and step index
    setShowListView(true); // Open the list-view-container
  }

  return (
    <div className="jobIntegrationContainer">
      <Header />
      <div className="createCancel">
        <div className="details">
          <div>{Listjob.name}</div>
          <div>{Listjob.description}</div>
          <div>{Listjob.cron}</div>
        </div>
        <div className="buttons">
          <button onClick={() =>submitData()}>Submit</button>
          <button>Cancel</button>
        </div>
      </div>

      <div className="row m-0">
        <div className="col-7">
          {/* If stepList is empty, show an initial "+" button */}
          {stepList.length === 0 && (
            <div
              className="initial-add-button"
              style={{
                cursor: "pointer",
                color: "green",
                marginBottom: "10px",
                textAlign: "center",
              }}
              onClick={() => toggleListView(null)}
            >
              +
            </div>
          )}

          {/* Display grouped steps with + buttons */}
          {stepList.map((group, groupIndex) => (
            <div
              key={groupIndex}
              className="step-group"
              style={{ marginBottom: "20px" }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                {group.map((data, stepIndex) => (
                  <div
                    key={stepIndex}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      marginBottom: "10px",
                      width: "100%",
                    }}
                  >
                    {/* The step content */}
                    <div
                      className="details-data"
                      style={{ flexGrow: 1, width: "100%" }}
                    >
                      <div className="title">{data.operator_name}</div>
                      <div className="description">{data.description}</div>
                    </div>

                    {/* + button to the right of the step */}
                    <div
                      className="add-button-right"
                      style={{
                        cursor: "pointer",
                        color: "blue",
                        marginLeft: "10px",
                        marginRight: "10px",
                      }}
                      onClick={() =>
                        toggleListView(groupIndex, stepIndex, "right")
                      } // Open list-view to add a step to the right
                    >
                      +
                    </div>
                  </div>
                ))}
              </div>

              {/* + button below the current group */}
              <div
                className="add-step-button"
                style={{
                  cursor: "pointer",
                  color: "green",
                  marginTop: "10px",
                  textAlign: "center",
                }}
                onClick={() => toggleListView(groupIndex, null, "below")} // Open list-view to add a step below the group
              >
                +
              </div>
            </div>
          ))}
        </div>

        {/* List-view-container toggle and content */}
        <div className="col-5">
          {/* Conditionally render the list-view-container */}
          {showListView && (
            <div className="list-view-container">
              <div className="header">Add an Action</div>
              <div
                className="modal"
                style={{ display: show ? "block" : "none" }}
              >
                <div className="input-container">
                  <input
                    type="text"
                    placeholder="Task Name"
                    value={taskName}
                    onChange={(e) => setTaskName(e.target.value)}
                  />
                  <input
                    type="text"
                    placeholder="Job Description"
                    value={taskParams}
                    onChange={(e) => settaskParams(e.target.value)}
                  />
                </div>
                <button onClick={handleNext}>Next</button>
              </div>
              <input type="search" />
              <div className="details">
                {IntegrationData.map((data: jobIntegration, index) => (
                  <div
                    key={index}
                    className="details-data"
                    onClick={
                      () => {
                        openModal();
                        setJobdata(data);
                      }
                      // createObject(data)
                    }
                  >
                    <div className="title">{data.operator_name}</div>
                    <div className="description">{data.description}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
