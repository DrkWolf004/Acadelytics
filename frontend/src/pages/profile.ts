import { getAuthToken, getAuthUser, setAuthStorage, getTheme, clearAuthStorage } from '../hooks/useLocalStorage'
import { renderHeaderControls } from '../app'
import { deleteUser, getUserById, updateUser } from '../services/userService'
import { showConfirmationPopup } from '../modal'
import type { AuthResponse, UserPayload, User } from '../types'

function renderProfileForm(root: HTMLElement, userData: User, token: string) {
  root.innerHTML = `
    <main class="page page-profile">
      <aside class="sidebar" id="sidebar">
        <div class="sidebar-inner">
          <div class="sidebar-header">
            <button id="sidebar-close" class="sidebar-close" aria-label="Cerrar">←</button>
            <div class="sidebar-brand">Acadelytics</div>
          </div>
          <nav class="sidebar-nav"></nav>
          <div class="sidebar-spacer"></div>
          <button id="sidebar-logout" class="sidebar-logout">Cerrar sesión</button>
        </div>
      </aside>

      <section class="auth-card">
        <div class="auth-header" style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;">
          <div style="display:flex;align-items:center;gap:12px;flex:1;min-width:0;">
            <button id="nav-toggle" class="nav-toggle" aria-label="Abrir menú">☰</button>
            <h1>Mi perfil</h1>
          </div>
          <div id="header-controls" class="header-controls"></div>
        </div>
        <div class="profile-meta">
          <div><strong>Rol actual:</strong> ${userData.rol}</div>
          <div><strong>Cambios restantes de rol:</strong> ${userData.role_changes_remaining}</div>
        </div>
        <form id="profile-form" class="auth-form">
          <label>
            Nombre
            <input type="text" name="nombre" value="${userData.nombre}" required />
          </label>
          <label>
            Apellido
            <input type="text" name="apellido" value="${userData.apellido}" required />
          </label>
          <label>
            Correo electrónico
            <input type="email" name="correo" value="${userData.correo}" required />
          </label>
          <label>
            Rol actual
            ${userData.rol === 'Admin' ? `
              <div class="static-value">${userData.rol}</div>
            ` : `
              <select name="rol" ${userData.role_changes_remaining <= 0 ? 'disabled' : ''}>
                <option value="Alumno" ${userData.rol === 'Alumno' ? 'selected' : ''}>Alumno</option>
                <option value="Profesor" ${userData.rol === 'Profesor' ? 'selected' : ''}>Profesor</option>
              </select>
            `}
          </label>
          <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:12px;">
            <button id="delete-account" type="button" class="button danger outline">Eliminar cuenta</button>
          </div>
          <label>
            Nueva contraseña
            <input type="password" name="newPassword" placeholder="Dejar en blanco para mantenerla" minlength="8" />
          </label>
          <button type="submit" class="button primary">Guardar cambios</button>
        </form>
        <div id="profile-message" class="form-success"></div>
        <div id="profile-error" class="form-error"></div>
      </section>
    </main>
  `

  const navToggle = document.querySelector<HTMLButtonElement>('#nav-toggle')
  const sidebarClose = document.querySelector<HTMLButtonElement>('#sidebar-close')
  navToggle?.addEventListener('click', () => document.body.classList.add('sidebar-open'))
  sidebarClose?.addEventListener('click', () => document.body.classList.remove('sidebar-open'))

  const sidebarNav = document.querySelector<HTMLDivElement>('.sidebar-nav')
  if (sidebarNav) {
    sidebarNav.innerHTML = `
      <a href="#/dashboard" data-router class="nav-link">Inicio</a>
      <a href="#/profile" data-router class="nav-link">Perfil</a>
      ${userData.rol === 'Admin' ? '<a href="#/admin/users" data-router class="nav-link">Usuarios</a>' : ''}
    `
  }

  const sidebarLogout = document.querySelector<HTMLButtonElement>('#sidebar-logout')
  const performLogout = () => {
    clearAuthStorage()
    window.location.hash = '#/login'
  }
  sidebarLogout?.addEventListener('click', performLogout)

  const form = document.querySelector<HTMLFormElement>('#profile-form')
  const deleteButton = document.querySelector<HTMLButtonElement>('#delete-account')
  const message = document.querySelector<HTMLDivElement>('#profile-message')
  const error = document.querySelector<HTMLDivElement>('#profile-error')

  deleteButton?.addEventListener('click', async () => {
    if (!error) return
    error.textContent = ''

    const confirmed = await showConfirmationPopup(
      '¿Deseas eliminar tu cuenta? Esta acción no se puede deshacer.',
      'Eliminar cuenta',
    )
    if (!confirmed) return

    const result = await deleteUser(userData.id)
    if (!result.ok) {
      error.textContent = result.error || 'No se pudo eliminar la cuenta.'
      return
    }

    clearAuthStorage()
    window.location.hash = '#/login'
  })

  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    if (!form || !error || !message) return
    error.textContent = ''
    message.textContent = ''

    const formData = new FormData(form)
    const payload: UserPayload = {
      nombre: formData.get('nombre')?.toString().trim() || '',
      apellido: formData.get('apellido')?.toString().trim() || '',
      correo: formData.get('correo')?.toString().trim() || '',
      rol: formData.get('rol')?.toString().trim() || userData.rol,
    }

    const selectedRole = payload.rol
    if (selectedRole !== userData.rol && userData.role_changes_remaining <= 0) {
      error.textContent = 'No quedan cambios de rol disponibles.'
      return
    }

    const newPassword = formData.get('newPassword')?.toString().trim() || ''
    if (newPassword) {
      payload.newPassword = newPassword
    }

    try {
      const result = await updateUser(userData.id, payload)
      if (!result.ok || !result.data) {
        error.textContent = result.error || 'No se pudo actualizar el perfil.'
        return
      }
      const updatedUser = result.data as User
      setAuthStorage(token, {
        id: updatedUser.id,
        nombre: updatedUser.nombre,
        apellido: updatedUser.apellido,
        correo: updatedUser.correo,
        rol: updatedUser.rol,
        role_changes_remaining: updatedUser.role_changes_remaining,
        token,
      } as AuthResponse)
      message.textContent = 'Perfil actualizado correctamente.'
      renderProfilePage(root)
    } catch {
      error.textContent = 'Error de conexión con el servidor.'
    }
  })
}

export async function renderProfilePage(root: HTMLElement) {
  const currentUser = getAuthUser()
  const token = getAuthToken()
  if (!currentUser || !token) {
    window.location.hash = '#/login'
    return
  }

  const result = await getUserById(currentUser.id)
  if (!result.ok || !result.data) {
    root.innerHTML = `
      <main class="page page-profile">
        <section class="auth-card">
          <div class="auth-header">
            <h1>Mi perfil</h1>
            <div id="header-controls" class="header-controls"></div>
          </div>
          <p class="form-error">No se pudo cargar el perfil.</p>
        </section>
      </main>
    `
    renderHeaderControls(getTheme())
    return
  }

  renderProfileForm(root, result.data, token)
  renderHeaderControls(getTheme())
}
