import type { AuthResponse, RequestResult } from '../types'
import { getAuthToken } from '../hooks/useLocalStorage'

const API_BASE = (import.meta.env.VITE_BASE_URL || 'http://localhost:5000/api').replace(/\/$/, '')

async function request<T>(url: string, options: RequestInit): Promise<RequestResult<T>> {
  try {
    const response = await fetch(`${API_BASE}${url}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers ?? {}),
      },
    })

    const json = await response.json()

    if (!response.ok) {
      return {
        ok: false,
        error: json.message || 'Error en la solicitud',
      }
    }

    return {
      ok: true,
      data: json.data as T,
    }
  } catch (error) {
    return {
      ok: false,
      error: 'No se pudo conectar al servidor',
    }
  }
}

function authHeaders(): Record<string, string> {
  const token = getAuthToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function post<T>(url: string, body: unknown): Promise<RequestResult<T>> {
  return request<T>(url, {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

export async function authPost(url: string, body: unknown): Promise<RequestResult<AuthResponse>> {
  return post<AuthResponse>(url, body)
}

export async function getAuth<T>(url: string): Promise<RequestResult<T>> {
  return request<T>(url, {
    method: 'GET',
    headers: authHeaders(),
  })
}

export async function postAuth<T>(url: string, body: unknown): Promise<RequestResult<T>> {
  return request<T>(url, {
    method: 'POST',
    body: JSON.stringify(body),
    headers: authHeaders(),
  })
}

export async function putAuth<T>(url: string, body: unknown): Promise<RequestResult<T>> {
  return request<T>(url, {
    method: 'PUT',
    body: JSON.stringify(body),
    headers: authHeaders(),
  })
}

export async function deleteAuth<T>(url: string): Promise<RequestResult<T>> {
  return request<T>(url, {
    method: 'DELETE',
    headers: authHeaders(),
  })
}
