import { useEffect, useState } from 'react'
import { createChild, listChildren, listRides } from '../lib/api'

export default function Dashboard() {
	const [children, setChildren] = useState<any[]>([])
	const [rides, setRides] = useState<any[]>([])
	const [name, setName] = useState('')
	const [school, setSchool] = useState('')
	const [klass, setKlass] = useState('')

	useEffect(() => {
		refresh()
	}, [])

	async function refresh() {
		try {
			const [kids, r] = await Promise.all([listChildren(), listRides()])
			setChildren(kids)
			setRides(r)
		} catch {}
	}

	async function addChild() {
		if (!name) return
		await createChild({ full_name: name, school_name: school || undefined, class_level: klass || undefined })
		setName(''); setSchool(''); setKlass('')
		refresh()
	}

	return (
		<div style={{ maxWidth: 900, margin: '2rem auto', fontFamily: 'Inter, system-ui, Arial' }}>
			<h2>Parent Dashboard</h2>
			<section>
				<h3>Children</h3>
				<ul>
					{children.map((c) => (
						<li key={c.id}>{c.full_name} {c.school_name ? `- ${c.school_name}` : ''} {c.class_level ? `(${c.class_level})` : ''}</li>
					))}
				</ul>
				<div style={{ display: 'flex', gap: 8 }}>
					<input placeholder="Full name" value={name} onChange={(e) => setName(e.target.value)} />
					<input placeholder="School" value={school} onChange={(e) => setSchool(e.target.value)} />
					<input placeholder="Class" value={klass} onChange={(e) => setKlass(e.target.value)} />
					<button onClick={addChild}>Add Child</button>
				</div>
			</section>
			<section>
				<h3>Recent Rides</h3>
				<ul>
					{rides.map((r) => (
						<li key={r.id}>{r.pickup_location} → {r.dropoff_location} [{r.status}]</li>
					))}
				</ul>
			</section>
		</div>
	)
}