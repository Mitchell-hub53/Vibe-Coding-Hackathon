import { useEffect, useState } from 'react'
import { createRide, listChildren } from '../lib/api'

export default function BookRide() {
	const [children, setChildren] = useState<any[]>([])
	const [childId, setChildId] = useState<number | null>(null)
	const [pickup, setPickup] = useState('')
	const [dropoff, setDropoff] = useState('')
	const [scheduled, setScheduled] = useState('')
	const [message, setMessage] = useState('')

	useEffect(() => {
		listChildren().then(setChildren).catch(() => {})
	}, [])

	async function submit() {
		if (!childId || !pickup || !dropoff) return
		await createRide({ child_id: childId, pickup_location: pickup, dropoff_location: dropoff, scheduled_time: scheduled || undefined })
		setMessage('Ride created successfully')
		setPickup(''); setDropoff(''); setScheduled('')
	}

	return (
		<div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'Inter, system-ui, Arial' }}>
			<h2>Book a Ride</h2>
			<select onChange={(e) => setChildId(Number(e.target.value))} defaultValue="">
				<option value="" disabled>Select Child</option>
				{children.map((c) => (
					<option key={c.id} value={c.id}>{c.full_name}</option>
				))}
			</select>
			<input placeholder="Pickup location" value={pickup} onChange={(e) => setPickup(e.target.value)} />
			<input placeholder="Dropoff location" value={dropoff} onChange={(e) => setDropoff(e.target.value)} />
			<input type="datetime-local" value={scheduled} onChange={(e) => setScheduled(e.target.value)} />
			<button onClick={submit}>Create</button>
			{message && <p style={{ color: 'green' }}>{message}</p>}
		</div>
	)
}