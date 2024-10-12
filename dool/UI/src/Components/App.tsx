import { useState } from 'react'
import reactLogo from '../assets/react.svg'
import viteLogo from '/electron-vite.animate.svg'
import '../App.css'
import Listjob from './Listjob'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <Listjob/>
        </div>
    </>
  )
}

export default App
