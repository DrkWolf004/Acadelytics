export type LoginPayload = {
  correo: string
  password: string
}

export type RegisterPayload = {
  nombre: string
  apellido: string
  correo: string
  password: string
}

export type AuthResponse = {
  id: number
  nombre: string
  apellido: string
  correo: string
  rol: string
  token: string
}

export type RequestResult<T> = {
  ok: boolean
  data?: T
  error?: string
}
