import { useState } from 'react'
import { signIn, signUp } from '../services/supabase'

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [isSignUp, setIsSignUp] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setMessage('')

    const normalizedEmail = email.trim().toLowerCase()
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    if (!emailPattern.test(normalizedEmail)) {
      setError('Enter a valid email address, such as name@example.com.')
      return
    }
    if (password.length < 6) {
      setError('Password must contain at least 6 characters.')
      return
    }

    setIsSubmitting(true)
    try {
      const action = isSignUp ? signUp : signIn
      const { data, error } = await action(normalizedEmail, password)

      if (error) {
        const knownErrors = {
          'Email address is invalid': 'Enter a valid email address accepted by Supabase.',
          'Email address or password is invalid': 'Email or password is incorrect.',
          'Password should be at least 6 characters': 'Password must contain at least 6 characters.',
          'User already registered': 'An account with this email already exists. Try signing in.',
        }
        setError(knownErrors[error.message] || error.message)
        return
      }

      if (isSignUp && !data.session) {
        setMessage('Account created. Check your email to confirm your account, then sign in.')
      }
    } catch (submitError) {
      setError(submitError.message || 'Unable to connect to the authentication service.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
      <h1>{isSignUp ? 'Create your account' : 'Welcome back'}</h1>
      <p>{isSignUp ? 'Start your SkillSetu journey.' : 'Sign in to continue to SkillSetu.'}</p>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
        required
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        required
      />

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Please wait...' : isSignUp ? 'Create account' : 'Sign in'}
      </button>

      {error && <p>{error}</p>}
      {message && <p>{message}</p>}

      <button type="button" onClick={() => setIsSignUp(!isSignUp)}>
        {isSignUp ? 'Already have an account?' : 'Create an account'}
      </button>
      </form>
    </main>
  )
}

export default Login