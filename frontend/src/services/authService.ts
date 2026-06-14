import { authPost } from './api'
import type { AuthResponse, LoginPayload, RegisterPayload } from '../types'

export async function login(payload: LoginPayload) {
  return authPost('/auth/login', payload)
}

export async function register(payload: RegisterPayload) {
  return authPost('/auth/register', payload)
}

export type AuthResult = {
  ok: boolean
  data?: AuthResponse
  error?: string
}
