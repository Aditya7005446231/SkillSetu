import { useState } from 'react'
import { signIn, signUp } from '../services/supabase'

function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [isSignUp, setIsSignUp] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setMessage('')

    const action = isSignUp ? signUp : signIn
    const { data, error } = await action(email, password)

    if (error) {
      setError(error.message)
      return
    }

    if (isSignUp && !data.session) {
      setMessage('Account created. Check your email to confirm your account, then sign in.')
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

      <button type="submit">
        {isSignUp ? 'Create account' : 'Sign in'}
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