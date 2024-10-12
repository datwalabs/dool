import React, { useState } from "react";
import jobIntegrationData from "../Data/JobIntegration";
import Header from "./Header/header";
import "../listjob.scss";
import { useLocation } from "react-router-dom";
import { jobIntegration } from "../Interface/IJobIntegration";

export default function EditJobIntegration() {
  const [IntegrationData, setIntegrationData] = useState(jobIntegrationData);
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

  const location = useLocation();
  const Listjob = location.state; // Access the passed data here
  console.log(Listjob[0]);

  // Create object and close the list view
  function createObject(data: jobIntegration) {
    const { groupIndex, stepIndex, position } = currentStepIndex;

    setSteplist((prevList) => {
      const newList = [...prevList];

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
      console.log(newList);
      return newList;
    });

    setShowListView(false); // Close the list-view-container after adding a step
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
        <div>{Listjob.job_id}</div>
        <div>{Listjob.job_name}</div>
        <div>{Listjob.cron}</div>
        </div>
        <div className="buttons">
        <button>Submit</button>
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
                      width:"100%"

                    }}
                  >
                    {/* The step content */}
                    <div className="details-data" style={{ flexGrow: 1, width: "100%" }}>
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
                        marginRight : "10px"
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
              <input type="search" />
              <div className="details">
                {IntegrationData.map((data: jobIntegration, index) => (
                  <div
                    key={index}
                    className="details-data"
                    onClick={() => createObject(data)}
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
