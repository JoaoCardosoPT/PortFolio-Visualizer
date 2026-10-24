import { useState } from "react"

export default function Tracker(){
  const [portfolios, Setportfolios] = useState([])
  const [portfolioName, SetportfolioName] = useState('')
  
  function portcreation(event){
    event.preventDefault()

    const name = portfolioName.trim()
    if (!name) return
    
    // A dictionary with the keys and values we want
    const newPortfolio = {
      id: crypto.randomUUID(),
      name,
      holdihgs: [],
    }
    // Creates a new array containing the existing portfolios and the new one
    Setportfolios((previous) => [...previous, newPortfolio])
    SetportfolioName('')

  }

  return (
    <main>
     <h1>Tracker</h1>
      <form onSubmit={portcreation}>
        <label htmlFor="Portfolio-Name">Portfolio Name</label>
        <input
          id="Portfolio-Name" type="text" placeholder="e.g Long Term" value={portfolioName} onChange={(event) => portcreation(event.target.value)}
        required
        />
        <button type="submit" disabled={!portfolioName.trim()}>Create</button>
      </form>

      <ul>
        {portfolios.map((portfolio) => (
          <li key={portfolio.id}>{portfolio.name}</li>
        ))}
      </ul>
    </main>
  )
}
