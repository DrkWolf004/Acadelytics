import type { AuthResponse } from '../types'

const TOKEN_KEY = 'acadelytics_token'
const USER_KEY = 'acadelytics_user'
const THEME_KEY = 'acadelytics_theme'

export function getTheme(): 'light' | 'dark' {
  const stored = localStorage.getItem(THEME_KEY)
  return stored === 'dark' ? 'dark' : 'light'
}

export function setTheme(theme: 'light' | 'dark') {
  localStorage.setItem(THEME_KEY, theme)

  const root = document.documentElement
  if (theme === 'dark') {
    root.classList.add('theme-dark')
  } else {
    root.classList.remove('theme-dark')
  }
}

export function setAuthStorage(token: string, authData: AuthResponse) {
  localStorage.setItem(TOKEN_KEY, token)
  localStorage.setItem(USER_KEY, JSON.stringify(authData))
}

export function getAuthToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function getAuthUser() {
  const raw = localStorage.getItem(USER_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as AuthResponse
  } catch {
    return null
  }
}

export function clearAuthStorage() {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
}

export function initializeTheme() {
  setTheme(getTheme())
}

export type ClassroomInvite = {
  id: string
  inviterNombre: string
  inviterApellido: string
  classroomName: string
  createdAt: string
}

const NOTIF_KEY = 'acadelytics_notifications'

export function getNotifications(): ClassroomInvite[] {
  const raw = localStorage.getItem(NOTIF_KEY)
  if (!raw) return []
  try {
    return JSON.parse(raw) as ClassroomInvite[]
  } catch {
    return []
  }
}

export function setNotifications(notifs: ClassroomInvite[]) {
  localStorage.setItem(NOTIF_KEY, JSON.stringify(notifs))
}

export function addNotification(n: ClassroomInvite) {
  const arr = getNotifications()
  arr.unshift(n)
  setNotifications(arr)
}

export function removeNotification(id: string) {
  const arr = getNotifications().filter(x => x.id !== id)
  setNotifications(arr)
}

export function clearNotifications() {
  localStorage.removeItem(NOTIF_KEY)
}
