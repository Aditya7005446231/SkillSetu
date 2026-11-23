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
