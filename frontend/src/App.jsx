import { useState } from 'react'

// Connect the Ui to the python folder
export default function App() {
  const [symbol, setSymbol] = useState('')

  function handleSearch(event) {
    event.preventDefault()
    console.log('Searching for:', symbol)
  }

  return (
    <main>
      <h1>Portfolio Tracker</h1>
      <input id="symbol" type="text" placeholder='e.g BTC'/>

      <button type="button">Search</button>
    </main>
  )
}
