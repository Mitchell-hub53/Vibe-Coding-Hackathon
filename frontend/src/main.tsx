import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import App from './pages/App'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import BookRide from './pages/BookRide'
import Incidents from './pages/Incidents'

const router = createBrowserRouter([
	{ path: '/', element: <App /> },
	{ path: '/login', element: <Login /> },
	{ path: '/dashboard', element: <Dashboard /> },
	{ path: '/book', element: <BookRide /> },
	{ path: '/incidents', element: <Incidents /> },
])

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
	<React.StrictMode>
		<RouterProvider router={router} />
	</React.StrictMode>,
)