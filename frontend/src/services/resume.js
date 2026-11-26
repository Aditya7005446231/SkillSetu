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
    timeout: 120000,
  })

  return response.data
}

export async function getStudentResumes() {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session) return []

  const response = await api.get('/api/resumes', {
    headers: { Authorization: `Bearer ${session.access_token}` },
  })
  return response.data
}

export async function saveManualProfile(profileData) {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session) throw new Error('Not authenticated')

  const response = await api.post('/api/resumes/manual', profileData, {
    headers: { Authorization: `Bearer ${session.access_token}` },
  })
  return response.data
}

export async function activateResume(resumeId) {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session) throw new Error('Not authenticated')

  const response = await api.post(`/api/resumes/${resumeId}/activate`, {}, {
    headers: { Authorization: `Bearer ${session.access_token}` },
  })
  return response.data
}
