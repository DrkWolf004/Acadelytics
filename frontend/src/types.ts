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

export type Classroom = {
  id: number
  nombre: string
  type: string
  class_folder_id: number | null
  create_at: string
  update_at: string
}

export type ClassroomMember = {
  id: number
  nombre: string
  apellido: string
  correo: string
  rol: string
}

export type FileRecord = {
  id: number
  class_folder_id: number
  uploaded_by_id?: number | null
  filename: string
  secure_name: string
  filepath: string
  upload_at: string
}

export type RequestResult<T> = {
  ok: boolean
  data?: T
  error?: string
}
