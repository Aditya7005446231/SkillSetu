import api from './api'
import { supabase } from './supabase'

export async function getRecommendedOpportunities(filters = {}) {
  const {
    data: { session },
    error,
  } = await supabase.auth.getSession()

  if (error) throw error
  if (!session?.access_token) {
    throw new Error('You must be signed in to view recommendations.')
  }

  const response = await api.get('/api/opportunities/recommended', {
    params: filters,
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  })
  return response.data.recommendations || []
}

export async function getLearningRoadmap() {
  const {
    data: { session },
    error,
  } = await supabase.auth.getSession()

  if (error) throw error
  if (!session?.access_token) {
    throw new Error('You must be signed in to view your learning roadmap.')
  }

  const response = await api.get('/api/learning-roadmap', {
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  })
  return response.data
}

export async function saveLearningProgress(progress) {
  const {
    data: { session },
    error,
  } = await supabase.auth.getSession()

  if (error) throw error
  if (!session?.access_token) {
    throw new Error('You must be signed in to save learning progress.')
  }

  const response = await api.put('/api/learning-progress', progress, {
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  })
  return response.data.progress
}

export async function getInstitutionalSkills(category = '') {
  const params = {}
  if (category) params.category = category
  const response = await api.get('/api/institution/skills', { params })
  return response.data
}

export async function getSavedOpportunities(limit = 20) {
  const {
    data: { session },
    error,
  } = await supabase.auth.getSession()

  if (session && session.access_token) {
    try {
      const response = await api.get('/api/opportunities/saved', {
        params: { limit },
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      })
      return response.data
    } catch (e) {
      console.warn('Saved opportunities failed:', e)
    }
  }

  // Fallback
  return []
}

export async function sendChatMessage(message, profile = {}) {
  const {
    data: { session },
  } = await supabase.auth.getSession()

  const payload = { message, profile }

  if (session && session.access_token) {
    try {
      const response = await api.post('/api/chat', payload, {
        headers: { Authorization: `Bearer ${session.access_token}` },
      })
      return response.data
    } catch (err) {
      console.warn('Primary chat failed, using local endpoint:', err)
    }
  }

  const response = await api.post('/api/chat-local', payload)
  return response.data
}
