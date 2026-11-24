import api from './api'
import { supabase } from './supabase'

export async function getRecommendedOpportunities(filters = {}) {
  const {
    data: { session },
    error,
  } = await supabase.auth.getSession()

  if (error) throw error
  if (!session) throw new Error('You must be signed in to view recommendations.')

  const response = await api.get('/api/opportunities/recommended', {
    params: filters,
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  })

  return response.data
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

  if (error) throw error
  if (!session) throw new Error('You must be signed in to view saved opportunities.')

  const response = await api.get('/api/opportunities/saved', {
    params: { limit },
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  })

  return response.data
}

export async function sendChatMessage(message) {
  const {
    data: { session },
    error,
  } = await supabase.auth.getSession()

  if (error) throw error
  if (!session) throw new Error('You must be signed in to chat with your career copilot.')

  const response = await api.post(
    '/api/chat',
    { message },
    {
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    }
  )

  return response.data
}

