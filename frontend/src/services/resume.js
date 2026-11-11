import api from './api'
import { supabase } from './supabase'

export async function analyzeResume(file) {
  const {
    data: { session },
    error: sessionError,
  } = await supabase.auth.getSession()

  if (sessionError) {
    throw sessionError
  }

  if (!session) {
    throw new Error('You must be signed in to analyze a resume.')
  }

  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post('/api/resume/analyze', formData, {
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  })

  return response.data
}
