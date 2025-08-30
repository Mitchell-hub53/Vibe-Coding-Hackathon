import { Link } from 'react-router-dom'

export default function App() {
	return (
		<div style={{ maxWidth: 720, margin: '2rem auto', fontFamily: 'Inter, system-ui, Arial' }}>
			<h1>SafiriSchola</h1>
			<p>School transportation with USSD access, in-vehicle camera surveillance, and a red emergency button.</p>
			<nav style={{ display: 'grid', gap: 8 }}>
				<Link to="/login">Login</Link>
				<Link to="/dashboard">Parent Dashboard</Link>
				<Link to="/book">Book a Ride</Link>
				<Link to="/incidents">Incidents</Link>
			</nav>
		</div>
	)
}