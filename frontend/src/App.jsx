import { useEffect, useState } from 'react'

const box = { maxWidth: 640, margin: '2rem auto', padding: '0 1rem', fontFamily: 'sans-serif' }

export default function App() {
  const [status, setStatus] = useState('перевірка...')
  const [items, setItems] = useState([])
  const [error, setError] = useState('')
  const [form, setForm] = useState({ amount: '', category: 'Інші витрати', description: '' })

  async function load() {
    try {
      const health = await fetch('/api/health')
      setStatus(health.ok ? 'працює' : 'недоступний')
      const response = await fetch('/api/transactions')
      setItems(await response.json())
      setError('')
    } catch (e) {
      setStatus('недоступний')
      setError('Не вдалося зв’язатися з API')
    }
  }

  useEffect(() => {
    load()
  }, [])

  async function submit(event) {
    event.preventDefault()
    const response = await fetch('/api/transactions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount: Number(form.amount),
        category: form.category || 'Інші витрати',
        description: form.description,
      }),
    })
    if (!response.ok) {
      setError('Не вдалося зберегти витрату')
      return
    }
    setForm({ ...form, amount: '', description: '' })
    load()
  }

  return (
    <div style={box}>
      <h1>FinWise</h1>
      <p>Стан API: <b>{status}</b></p>
      {error && <p style={{ color: 'crimson' }}>{error}</p>}

      <h2>Додати витрату готівкою</h2>
      <form onSubmit={submit} style={{ display: 'grid', gap: 8 }}>
        <input
          type="number" step="0.01" min="0.01" required placeholder="Сума"
          value={form.amount}
          onChange={(e) => setForm({ ...form, amount: e.target.value })}
        />
        <input
          placeholder="Категорія"
          value={form.category}
          onChange={(e) => setForm({ ...form, category: e.target.value })}
        />
        <input
          placeholder="Опис (необов’язково)"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <button type="submit">Додати</button>
      </form>

      <h2>Останні операції</h2>
      {items.length === 0 ? (
        <p>Поки що немає жодної операції.</p>
      ) : (
        <ul>
          {items.map((t) => (
            <li key={t.id}>
              {t.amount} грн, {t.category}
              {t.description ? ` (${t.description})` : ''}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
