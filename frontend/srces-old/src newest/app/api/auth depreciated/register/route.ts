import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const userData = await request.json()
    console.log('Frontend sending data to Flask:', userData)

    const response = await fetch('http://localhost:5000/auth/register', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    })

    console.log('Flask response status:', response.status)
    
    if (!response.ok) {
      const errorText = await response.text()
      console.log('Flask error response:', errorText)
      const errorData = await response.json().catch(() => ({}))
      return NextResponse.json(
        { error: errorData.message || 'Registration failed' },
        { status: response.status }
      )
    }

    const data = await response.json()
    console.log('Flask success response:', data)
    return NextResponse.json(data)
  } catch (error) {
    console.error('Register API error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}