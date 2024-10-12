import React from 'react'
import listjob from "../Data/ListJob"
import { Job, User, Operator, Task } from "../Interface/IListjob";
import "../listjob.scss"


export default function Listjob() {

    const listJob:[Job] = listjob;
  return (
    <div className='listJob-Container'>
        <div className='header'>
            <div className='logo'>
              
            </div>
            <div className='userDetails'>
            <div className='userName'>
                Welcome Sourajit
            </div>
            <div>
                Log out
            </div>
            </div>
        </div>


    </div>
  )
}
