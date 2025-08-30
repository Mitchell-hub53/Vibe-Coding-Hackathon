import { FormEvent, useState } from 'react'
import { login } from '../lib/api'

export default function Login() {
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [error, setError] = useState('')

	async function onSubmit(e: FormEvent) {
		e.preventDefault()
		try {
			await login(email, password)
			window.location.href = '/dashboard'
		} catch (err: any) {
			setError(err?.response?.data?.detail || 'Login failed')
		}
	}

	return (
		<div style={{ maxWidth: 420, margin: '2rem auto', fontFamily: 'Inter, system-ui, Arial' }}>
			<h2>Login</h2>
			<form onSubmit={onSubmit} style={{ display: 'grid', gap: 12 }}>
				<input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
				<input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
				<button type="submit">Sign In</button>
			</form>
			{error && <p style={{ color: 'crimson' }}>{error}</p>}
		</div>
	)
}