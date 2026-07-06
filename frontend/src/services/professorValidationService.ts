import type { RequestResult } from '../types'
import { getAuthToken } from '../hooks/useLocalStorage'
import { deleteAuth, getAuth, putAuth } from './api'

export type ProfessorValidationRequest = {
  id: number
  user_id: number
  requested_role: string
  status: string
  filename: string
  secure_name: string
  filepath: string
  review_comment: string | null
  create_at: string | null
  reviewed_at: string | null
  user: {
    id: number
    nombre: string
    apellido: string
    correo: string
    rol: string
  } | null
}

export async function submitProfessorValidation(file: File): Promise<RequestResult<ProfessorValidationRequest>> {
  const token = getAuthToken()
  if (!token) {
    return { ok: false, error: 'No autorizado' }
  }

  return new Promise((resolve) => {
    const formData = new FormData()
    formData.append('file', file)
    const xhr = new XMLHttpRequest()
    xhr.addEventListener('load', () => {
      if (xhr.status === 201 || xhr.status === 200) {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve({ ok: true, data: response.payload })
        } catch {
          resolve({ ok: false, error: 'Error al procesar la respuesta' })
        }
      } else {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve({ ok: false, error: response.message || 'Error al enviar la solicitud' })
        } catch {
          resolve({ ok: false, error: 'Error al enviar la solicitud' })
        }
      }
    })
    xhr.addEventListener('error', () => resolve({ ok: false, error: 'Error de conexión' }))
    xhr.open('POST', `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/professor-validations`)
    xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    xhr.send(formData)
  })
}

export async function getProfessorValidationRequests(status?: string): Promise<RequestResult<ProfessorValidationRequest[]>> {
  const params = new URLSearchParams()
  if (status) params.set('status', status)
  return getAuth<ProfessorValidationRequest[]>(`/professor-validations${params.toString() ? `?${params.toString()}` : ''}`)
}

export async function getProfessorValidationRequest(requestId: number): Promise<RequestResult<ProfessorValidationRequest>> {
  return getAuth<ProfessorValidationRequest>(`/professor-validations/${requestId}`)
}

export async function reviewProfessorValidationRequest(requestId: number, payload: { status: string; comment?: string }): Promise<RequestResult<ProfessorValidationRequest>> {
  return putAuth<ProfessorValidationRequest>(`/professor-validations/${requestId}/review`, payload)
}

export async function deleteProfessorValidationRequest(requestId: number): Promise<RequestResult<unknown>> {
  return deleteAuth<unknown>(`/professor-validations/${requestId}`)
}
