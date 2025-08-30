import { useState } from 'react'
import { reportIncident } from '../lib/api'

export default function Incidents() {
	const [source, setSource] = useState('button')
	const [message, setMessage] = useState('')

	async function send() {
		await reportIncident({ source })
		setMessage('Incident reported and ticket created')
	}

	return (
		<div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'Inter, system-ui, Arial' }}>
			<h2>Incidents</h2>
			<label>
				Source:
				<select value={source} onChange={(e) => setSource(e.target.value)}>
					<option value="button">Red Button (Student)</option>
					<option value="driver_app">Driver App SOS</option>
					<option value="system">System</option>
				</select>
			</label>
			<button onClick={send}>Report</button>
			{message && <p style={{ color: 'green' }}>{message}</p>}
		</div>
	)
}