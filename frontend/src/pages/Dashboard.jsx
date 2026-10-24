import { useState } from 'react'
import CandleChart from '../candlechart'

export default function App() {
  const [symbol, setSymbol] = useState('')
  const [quote, setQuote] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [candles, setCandles] = useState([])

  async function handleSearch(event) {
    event.preventDefault()

    const normalizedSymbol = symbol.trim().toUpperCase()
    setError('')
    setQuote(null)
    setCandles([])

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

      // Includes the coin symbol to USDT and saves 
      const pair = `${normalizedSymbol}USDT`
      const candleResponse = await fetch(`/api/candles?symbol=${encodeURIComponent(pair)}&interval=1h&limit=24` )
    
      if (!candleResponse.ok) {
        throw new Error('Not possible to obtain candle data')
      }
      const candleResult = await candleResponse.json()
      setCandles(candleResult.data)
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
        <input id="symbol" type="text" placeholder='e.g BTC' value={symbol} onChange={(event) => setSymbol(event.target.value)} />
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
      {candles.length > 0 && (
        <section className="chart-card" aria-labelledby="chart-title">
          <header className="chart-header">
            <div>
              <span className="chart-eyebrow">Price history</span>
              <h2 id="chart-title">{quote?.Symbol}<span> / USDT</span></h2>
              <p className="chart-description">{candles.length} hourly candles · Binance</p>
            </div>
            <span className="chart-interval">1 hour</span>
          </header>
          <CandleChart candles={candles} />
          <footer className="chart-footer">
            <div className="chart-legend" aria-label="Candle colors">
              <span><i className="chart-dot chart-dot-up" aria-hidden="true" />Price up</span>
              <span><i className="chart-dot chart-dot-down" aria-hidden="true" />Price down</span>
            </div>
            <span>Prices in USDT · Times in UTC</span>
          </footer>
        </section>
      )}
    </main>
  )
}
