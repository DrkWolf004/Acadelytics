import type { FileRecord } from '../types'
import { getAuthToken } from '../hooks/useLocalStorage'
import { deleteAuth, getAuth, postAuth, putAuth } from './api'

export async function getFilesByClassFolder(classFolderId: number): Promise<{ ok: boolean; data?: FileRecord[]; error?: string }> {
  return getAuth<FileRecord[]>(`/files?class_folder_id=${classFolderId}`)
}

export async function createFile(payload: {
  class_folder_id: number
  filename: string
  secure_name: string
  filepath: string
}): Promise<{ ok: boolean; data?: FileRecord; error?: string }> {
  return postAuth('/files', payload)
}

export async function uploadFile(
  classFolderId: number,
  file: File,
  onProgress?: (progress: number) => void
): Promise<{ ok: boolean; data?: FileRecord; error?: string }> {
  const token = getAuthToken()
  if (!token) {
    return { ok: false, error: 'No autorizado' }
  }

  const formData = new FormData()
  formData.append('file', file)

  return new Promise((resolve) => {
    const xhr = new XMLHttpRequest()

    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        const progress = Math.round((event.loaded / event.total) * 100)
        onProgress?.(progress)
      }
    })

    xhr.addEventListener('load', () => {
      if (xhr.status === 201 || xhr.status === 200) {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve({ ok: true, data: response.payload })
        } catch {
          resolve({ ok: false, error: 'Error al procesar respuesta' })
        }
      } else {
        try {
          const response = JSON.parse(xhr.responseText)
          resolve({ ok: false, error: response.message || 'Error al subir archivo' })
        } catch {
          resolve({ ok: false, error: 'Error desconocido' })
        }
      }
    })

    xhr.addEventListener('error', () => {
      resolve({ ok: false, error: 'Error de conexión' })
    })

    const url = `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/files/upload/${classFolderId}`
    xhr.open('POST', url)
    xhr.setRequestHeader('Authorization', `Bearer ${token}`)
    xhr.send(formData)
  })
}

export async function getFileRaw(fileId: number): Promise<{ ok: boolean; data?: Blob; error?: string }> {
  const token = getAuthToken()
  if (!token) {
    return { ok: false, error: 'No autorizado' }
  }

  const url = `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/files/${fileId}/raw`
  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    const contentType = response.headers.get('content-type') || ''
    if (contentType.includes('application/json')) {
      const body = await response.json()
      return { ok: false, error: body.message || 'No se pudo obtener el archivo.' }
    }
    return { ok: false, error: 'No se pudo obtener el archivo.' }
  }

  const blob = await response.blob()
  return { ok: true, data: blob }
}

export async function updateFile(fileId: number, payload: { filename?: string }): Promise<{ ok: boolean; data?: FileRecord; error?: string }> {
  return putAuth(`/files/${fileId}`, payload)
}

export async function deleteFile(fileId: number): Promise<{ ok: boolean; data?: unknown; error?: string }> {
  return deleteAuth<unknown>(`/files/${fileId}`)
}
