import { useState } from "react";
import Dashboard from './pages/Dashboard'
import Tracker from './pages/tracker'

export default function App()
{
  const [section, setSection] = useState('dashboard')

  return (
    <>
      <nav className="app-nav" aria-label="Main navigation">
        <button
          type="button"
          aria-pressed={section === 'dashboard'}
          onClick={() => setSection('dashboard')}
        >
          Dashboard
        </button>

        <button
          type="button"
          aria-pressed={section === 'tracker'}
          onClick={() => setSection('tracker')}
        >
          Tracker
        </button>
      </nav>

      <div hidden={section !== 'dashboard'}>
        <Dashboard />
      </div>

      <div hidden={section !== 'tracker'}>
        <Tracker />
      </div>
    </>
   )
}
