import axios from 'axios'

const api = axios.create({
	baseURL: '/api/v1',
})

api.interceptors.request.use((config) => {
	const token = localStorage.getItem('token')
	if (token) {
		config.headers = config.headers ?? {}
		config.headers.Authorization = `Bearer ${token}`
	}
	return config
})

export async function login(email: string, password: string) {
	const { data } = await api.post('/auth/login', { email, password })
	localStorage.setItem('token', data.access_token)
	return data
}

export async function register(payload: {
	email: string
	password: string
	full_name: string
	phone: string
	role?: 'parent' | 'driver' | 'admin'
}) {
	return api.post('/auth/register', payload)
}

export async function listChildren() {
	const { data } = await api.get('/parents/children')
	return data
}

export async function createChild(payload: {
	full_name: string
	school_name?: string
	class_level?: string
}) {
	const { data } = await api.post('/parents/children', payload)
	return data
}

export async function createRide(payload: {
	child_id: number
	pickup_location: string
	dropoff_location: string
	scheduled_time?: string
}) {
	const { data } = await api.post('/rides', payload)
	return data
}

export async function listRides() {
	const { data } = await api.get('/rides')
	return data
}

export async function reportIncident(payload: {
	source: string
	ride_id?: number
	child_id?: number
	driver_profile_id?: number
	vehicle_id?: number
	latitude?: number
	longitude?: number
	snapshot_url?: string
}) {
	const { data } = await api.post('/rides/incidents', payload)
	return data
}

export default api