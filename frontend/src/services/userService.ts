import type { RequestResult, User, UserPayload } from '../types'
import { deleteAuth, getAuth, postAuth, putAuth } from './api'

export async function getUserById(userId: number): Promise<RequestResult<User>> {
  return getAuth<User>(`/users/${userId}`)
}

export async function searchUsers(query: { correo?: string; id?: number }): Promise<RequestResult<User | User[]>> {
  const params = new URLSearchParams()
  if (query.id !== undefined) params.set('id', String(query.id))
  if (query.correo) params.set('correo', query.correo)
  return getAuth<User | User[]>(`/users?${params.toString()}`)
}

export async function getAllUsers(): Promise<RequestResult<User[]>> {
  return getAuth<User[]>('/users')
}

export async function createUser(payload: UserPayload): Promise<RequestResult<User>> {
  return postAuth<User>('/users', payload)
}

export async function updateUser(userId: number, payload: UserPayload): Promise<RequestResult<User>> {
  return putAuth<User>(`/users/${userId}`, payload)
}

export async function deleteUser(userId: number): Promise<RequestResult<unknown>> {
  return deleteAuth<unknown>(`/users/${userId}`)
}
