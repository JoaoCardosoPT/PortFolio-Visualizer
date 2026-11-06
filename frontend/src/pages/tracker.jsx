import { useState } from "react"

// TODO - Improve UI of the table
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
      holdings: [],
    }

    const exists = portfolios.some((portfolio) => portfolio.name.toLowerCase() === name.toLowerCase);
    if (exists) return;

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
          id="Portfolio-Name" type="text" placeholder="e.g Long Term" value={portfolioName} onChange={(event) => SetportfolioName(event.target.value)}
        required
        />
        <button type="submit">Create</button>
      </form>

      <tbody>
        {portfolios.map((portfolio) => (
          <tr key={portfolio.id}>
            <td>{portfolio.name}</td>
          </tr>
        ))}
      </tbody>
    </main>
  )
}
