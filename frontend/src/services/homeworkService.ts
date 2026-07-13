import type { Homework, HomeworkResponse } from '../types'
import { getAuthToken } from '../hooks/useLocalStorage'
import { deleteAuth, getAuth } from './api'

export async function getHomeworks(classroomId: number): Promise<{ ok: boolean; data?: Homework[]; error?: string }> {
  return getAuth<Homework[]>(`/homeworks?classroom_id=${classroomId}`)
}

export async function createHomework(payload: Record<string, unknown>, file?: File): Promise<{ ok: boolean; data?: Homework; error?: string }> {
  const token = getAuthToken()
  if (!token) return { ok: false, error: 'No autorizado' }

  const formData = new FormData()
  Object.entries(payload).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      formData.append(key, String(value))
    }
  })
  if (file) formData.append('file', file)

  return new Promise((resolve) => {
    const xhr = new XMLHttpRequest()
    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve({ ok: true, data: response.data as Homework })
        } catch {
          resolve({ ok: false, error: 'Error al procesar la respuesta' })
        }
      } else {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve({ ok: false, error: response.message || 'Error al crear la tarea' })
        } catch {
          resolve({ ok: false, error: 'Error desconocido' })
        }
      }
    })
    xhr.addEventListener('error', () => resolve({ ok: false, error: 'Error de conexión' }))
    xhr.open('POST', `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/homeworks`)
    xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    xhr.send(formData)
  })
}

export async function updateHomework(homeworkId: number, payload: Record<string, unknown>, file?: File): Promise<{ ok: boolean; data?: Homework; error?: string }> {
  const token = getAuthToken()
  if (!token) return { ok: false, error: 'No autorizado' }

  const formData = new FormData()
  Object.entries(payload).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      formData.append(key, String(value))
    }
  })
  if (file) formData.append('file', file)

  return new Promise((resolve) => {
    const xhr = new XMLHttpRequest()
    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve({ ok: true, data: response.data as Homework })
        } catch {
          resolve({ ok: false, error: 'Error al procesar la respuesta' })
        }
      } else {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve({ ok: false, error: response.message || 'Error al actualizar la tarea' })
        } catch {
          resolve({ ok: false, error: 'Error desconocido' })
        }
      }
    })
    xhr.addEventListener('error', () => resolve({ ok: false, error: 'Error de conexión' }))
    xhr.open('PUT', `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/homeworks/${homeworkId}`)
    xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    xhr.send(formData)
  })
}

export async function deleteHomework(homeworkId: number): Promise<{ ok: boolean; data?: unknown; error?: string }> {
  return deleteAuth<unknown>(`/homeworks/${homeworkId}`)
}

export async function submitHomeworkResponse(homeworkId: number, payload: Record<string, unknown>, file?: File): Promise<{ ok: boolean; data?: HomeworkResponse; error?: string }> {
  const token = getAuthToken()
  if (!token) return { ok: false, error: 'No autorizado' }

  const formData = new FormData()
  Object.entries(payload).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      formData.append(key, String(value))
    }
  })
  if (file) formData.append('file', file)

  return new Promise((resolve) => {
    const xhr = new XMLHttpRequest()
    xhr.addEventListener('load', () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve({ ok: true, data: response.data as HomeworkResponse })
        } catch {
          resolve({ ok: false, error: 'Error al procesar la respuesta' })
        }
      } else {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve({ ok: false, error: response.message || 'Error al responder la tarea' })
        } catch {
          resolve({ ok: false, error: 'Error desconocido' })
        }
      }
    })
    xhr.addEventListener('error', () => resolve({ ok: false, error: 'Error de conexión' }))
    xhr.open('POST', `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/homeworks/${homeworkId}/responses`)
    xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    xhr.send(formData)
  })
}

export async function downloadHomeworkAttachment(homeworkId: number): Promise<{ ok: boolean; data?: Blob; error?: string }> {
  const token = getAuthToken()
  if (!token) return { ok: false, error: 'No autorizado' }
  const url = `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/homeworks/${homeworkId}/attachment`
  const response = await fetch(url, { headers: { Authorization: `Bearer ${token}` } })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    return { ok: false, error: body.message || 'No se pudo descargar el archivo' }
  }
  const blob = await response.blob()
  return { ok: true, data: blob }
}

export type HomeworkResponseWithStudent = {
  student_id: number
  student_name: string
  student_email: string
  submitted: boolean
  grade?: string | null
  response_id?: number | null
  explanation?: string | null
  filename?: string | null
  submitted_at?: string | null
}

export async function getHomeworkResponses(homeworkId: number): Promise<{ ok: boolean; data?: HomeworkResponseWithStudent[]; error?: string }> {
  return getAuth<HomeworkResponseWithStudent[]>(`/homeworks/${homeworkId}/responses`)
}

export async function gradeHomeworkResponse(homeworkId: number, responseId: number, grade: string): Promise<{ ok: boolean; data?: unknown; error?: string }> {
  const token = getAuthToken()
  if (!token) return { ok: false, error: 'No autorizado' }

  const url = `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/homeworks/${homeworkId}/responses/${responseId}/grade`
  const response = await fetch(url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ grade }),
  })

  const body = await response.json().catch(() => ({}))
  if (!response.ok) {
    return { ok: false, error: body.message || 'Error al calificar' }
  }
  return { ok: true, data: body.data }
}

export async function autoGradeMissingResponses(homeworkId: number): Promise<{ ok: boolean; data?: unknown; error?: string }> {
  const token = getAuthToken()
  if (!token) return { ok: false, error: 'No autorizado' }

  const url = `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/homeworks/${homeworkId}/auto-grade`
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
  })

  const body = await response.json().catch(() => ({}))
  if (!response.ok) {
    return { ok: false, error: body.message || 'Error al calificar' }
  }
  return { ok: true, data: body.data }
}

export async function downloadHomeworkResponseFile(homeworkId: number, responseId: number): Promise<{ ok: boolean; data?: Blob; error?: string }> {
  const token = getAuthToken()
  if (!token) return { ok: false, error: 'No autorizado' }
  const url = `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/homeworks/${homeworkId}/responses/${responseId}/file`
  const response = await fetch(url, { headers: { Authorization: `Bearer ${token}` } })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    return { ok: false, error: body.message || 'No se pudo descargar el archivo' }
  }
  const blob = await response.blob()
  return { ok: true, data: blob }
}

