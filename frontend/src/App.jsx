import { useState } from 'react'

export default function App() {
  const [symbol, setSymbol] = useState('')
  const [quote, setQuote] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSearch(event) {
    event.preventDefault()

    const normalizedSymbol = symbol.trim().toUpperCase()
    setError('')
    setQuote(null)

    if (!normalizedSymbol) {
      setError('Input some crypto Symbol')
      return
    }

    setLoading(true)
    try {
      const response = await fetch(
        `/api/quote?symbol=${encodeURIComponent(normalizedSymbol)}`
      )

      const result = await response.json()

      if (!response.ok) {
        throw new Error(
          typeof result.detail === 'string'
            ? result.detail
            : 'Data Not found'
        )
      }

      setQuote(result.data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main>
      <h1>Portfolio Tracker</h1>
      <form onSubmit={handleSearch}>
        <input id="symbol" type="text" placeholder='e.g BTC'value={symbol} onChange={(event) => setSymbol(event.target.value)}/>
        <button type="submit" disabled={loading}>Search</button>
      </form>

      {error && <p role='alert'>{error}</p>}
      {quote && (
        <section>
          <h2>{quote.Symbol}</h2>
          <p>Price: ${quote.Price.toFixed(2)}</p>
          <p>Updated: {quote.Time}</p>
        </section>
      )}
    </main>
  )
}
