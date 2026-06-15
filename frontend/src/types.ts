export type LoginPayload = {
  correo: string
  password: string
}

export type RegisterPayload = {
  nombre: string
  apellido: string
  correo: string
  password: string
  rol: string
}

export type AuthResponse = {
  id: number
  nombre: string
  apellido: string
  correo: string
  rol: string
  role_changes_remaining: number
  token: string
}

export type User = {
  id: number
  nombre: string
  apellido: string
  correo: string
  rol: string
  role_changes_remaining: number
  create_at: string
  update_at: string
}

export type UserPayload = {
  nombre: string
  apellido: string
  correo: string
  rol: string
  role_changes_remaining?: number
  password?: string
  newPassword?: string
}

export type RequestResult<T> = {
  ok: boolean
  data?: T
  error?: string
}
