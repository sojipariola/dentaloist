import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const authHeader = request.headers.get('Authorization')
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const token = authHeader.substring(7)
    
    // Verify the token with your Flask backend
    const response = await fetch('http://localhost:5000/auth/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      return NextResponse.json({ error: 'Invalid token' }, { status: 401 })
    }

    const userData = await response.json()
    return NextResponse.json({ user: userData })
  } catch (error) {
    console.error('Auth me error:', error)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}