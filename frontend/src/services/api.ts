import type { AuthResponse, RequestResult } from '../types'

const API_BASE = 'http://localhost:5000/api'

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

export async function post<T>(url: string, body: unknown): Promise<RequestResult<T>> {
  return request<T>(url, {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

export async function authPost(url: string, body: unknown): Promise<RequestResult<AuthResponse>> {
  return post<AuthResponse>(url, body)
}
