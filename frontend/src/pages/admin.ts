import { getAuthUser, getTheme, clearAuthStorage } from '../hooks/useLocalStorage'
import { renderHeaderControls } from '../app'
import { createUser, deleteUser, getAllUsers, searchUsers, updateUser } from '../services/userService'
import { showConfirmationPopup } from '../modal'
import type { User, UserPayload } from '../types'

function createModal(innerHtml: string, onClose: () => void): HTMLDivElement {
  const overlay = document.createElement('div')
  overlay.className = 'modal-overlay'

  const dialog = document.createElement('div')
  dialog.className = 'modal-dialog'
  dialog.innerHTML = innerHtml

  const closeIcon = document.createElement('button')
  closeIcon.type = 'button'
  closeIcon.className = 'modal-close'
  closeIcon.setAttribute('aria-label', 'Cerrar')
  closeIcon.textContent = '×'
  closeIcon.addEventListener('click', () => onClose())

  dialog.insertAdjacentElement('afterbegin', closeIcon)
  dialog.addEventListener('click', (event) => event.stopPropagation())
  overlay.addEventListener('click', () => onClose())

  overlay.appendChild(dialog)
  document.body.appendChild(overlay)
  return overlay
}

function openUserFormModal(title: string, user?: User) {
  return new Promise<UserPayload | null>((resolve) => {
    const existingValues = user
      ? {
          nombre: user.nombre,
          apellido: user.apellido,
          correo: user.correo,
          rol: user.rol,
        }
      : { nombre: '', apellido: '', correo: '', rol: 'Alumno' }
    const existingRoleChanges = user ? user.role_changes_remaining : 3

    const modal = createModal(
      `<h2>${title}</h2>
      <form id="user-modal-form" class="auth-form">
        <label>
          Nombre
          <input name="nombre" value="${existingValues.nombre}" required />
        </label>
        <label>
          Apellido
          <input name="apellido" value="${existingValues.apellido}" required />
        </label>
        <label>
          Correo electrónico
          <input type="email" name="correo" value="${existingValues.correo}" required />
        </label>
        <label>
          Rol
          <select name="rol" required>
            <option value="Alumno" ${existingValues.rol === 'Alumno' ? 'selected' : ''}>Alumno</option>
            <option value="Profesor" ${existingValues.rol === 'Profesor' ? 'selected' : ''}>Profesor</option>
            <option value="Admin" ${existingValues.rol === 'Admin' ? 'selected' : ''}>Admin</option>
          </select>
        </label>
        <label>
          Cambios de rol restantes
          <select name="role_changes_remaining" required>
            ${[0, 1, 2, 3]
              .map(
                (value) => `<option value="${value}" ${value === existingRoleChanges ? 'selected' : ''}>${value}</option>`,
              )
              .join('')}
          </select>
        </label>
        <label>
          ${user ? 'Nueva contraseña' : 'Contraseña'}
          <input type="password" name="password" placeholder="${user ? 'Opcional' : ''}" ${user ? '' : 'required minlength="8"'} />
        </label>
        <div style="display:flex;gap:12px;margin-top:16px;justify-content:flex-end;">
          <button type="submit" class="button primary">Guardar</button>
        </div>
      </form>`,
      () => {
        document.body.removeChild(modal)
        resolve(null)
      },
    )

    const form = modal.querySelector<HTMLFormElement>('#user-modal-form')
    form?.addEventListener('submit', (event) => {
      event.preventDefault()
      const formData = new FormData(form)
      const result: UserPayload = {
        nombre: formData.get('nombre')?.toString().trim() || '',
        apellido: formData.get('apellido')?.toString().trim() || '',
        correo: formData.get('correo')?.toString().trim() || '',
        rol: formData.get('rol')?.toString().trim() || 'Alumno',
      }
      const password = formData.get('password')?.toString().trim() || ''
      if (password) {
        if (user) result.newPassword = password
        else result.password = password
      }
      const roleChanges = Number(formData.get('role_changes_remaining')?.toString() || '3')
      if (!Number.isNaN(roleChanges)) {
        result.role_changes_remaining = Math.min(3, Math.max(0, roleChanges))
      }
      document.body.removeChild(modal)
      resolve(result)
    })
  })
}

function renderUsersTable(users: User[]) {
  if (users.length === 0) {
    return '<p>No se encontraron usuarios.</p>'
  }

  return `
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Apellido</th>
          <th>Correo</th>
          <th>Rol</th>
          <th>Cambios restantes</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        ${users
          .map(
            (user) => `
            <tr>
              <td>${user.id}</td>
              <td>${user.nombre}</td>
              <td>${user.apellido}</td>
              <td>${user.correo}</td>
              <td>${user.rol}</td>
              <td>${user.role_changes_remaining}</td>
              <td>
                <button class="button outline small icon-button edit-user" data-user-id="${user.id}" title="Editar usuario" aria-label="Editar usuario">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 20h9" />
                    <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z" />
                  </svg>
                </button>
                <button class="button danger small icon-button delete-user" data-user-id="${user.id}" title="Eliminar usuario" aria-label="Eliminar usuario">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 6h18" />
                    <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
                    <path d="M10 11v6" />
                    <path d="M14 11v6" />
                    <path d="M9 6V4h6v2" />
                  </svg>
                </button>
              </td>
            </tr>
          `,
          )
          .join('')}
      </tbody>
    </table>
  `
}

async function loadUserList(root: HTMLElement, filter?: { correo?: string; id?: number }) {
  const listContainer = document.querySelector<HTMLDivElement>('#admin-user-list')
  const errorContainer = document.querySelector<HTMLDivElement>('#admin-error')
  if (!listContainer || !errorContainer) return

  errorContainer.textContent = ''
  const result = filter ? await searchUsers(filter) : await getAllUsers()
  if (!result.ok) {
    errorContainer.textContent = result.error || 'No se pudo cargar la lista de usuarios.'
    listContainer.innerHTML = ''
    return
  }

  const users = result.data
    ? Array.isArray(result.data)
      ? result.data
      : [result.data]
    : []
  listContainer.innerHTML = renderUsersTable(users)
  attachUserActions(root)
}

function attachUserActions(root: HTMLElement) {
  const editButtons = Array.from(document.querySelectorAll<HTMLButtonElement>('.edit-user'))
  editButtons.forEach((button) => {
    button.addEventListener('click', async () => {
      const userId = Number(button.dataset.userId)
      const row = button.closest('tr')
      if (!row || isNaN(userId)) return
      const user: User = {
        id: userId,
        nombre: row.children[1].textContent?.trim() || '',
        apellido: row.children[2].textContent?.trim() || '',
        correo: row.children[3].textContent?.trim() || '',
        rol: row.children[4].textContent?.trim() || 'Alumno',
        role_changes_remaining: Number(row.children[5].textContent?.trim()) || 0,
        create_at: '',
        update_at: '',
      }
      const values = await openUserFormModal('Editar usuario', user)
      if (!values) return
      const result = await updateUser(userId, values)
      if (!result.ok) {
        const error = document.querySelector<HTMLDivElement>('#admin-error')
        if (error) error.textContent = result.error || 'No se pudo editar el usuario.'
        return
      }
      await loadUserList(root)
    })
  })

  const deleteButtons = Array.from(document.querySelectorAll<HTMLButtonElement>('.delete-user'))
  deleteButtons.forEach((button) => {
    button.addEventListener('click', async () => {
      const userId = Number(button.dataset.userId)
      if (isNaN(userId)) return

      const confirmed = await showConfirmationPopup('¿Deseas eliminar este usuario? Esta acción no se puede deshacer.', 'Eliminar usuario')
      if (!confirmed) return

      const result = await deleteUser(userId)
      if (!result.ok) {
        const error = document.querySelector<HTMLDivElement>('#admin-error')
        if (error) error.textContent = result.error || 'No se pudo eliminar el usuario.'
        return
      }
      await loadUserList(root)
    })
  })
}

export async function renderAdminPage(root: HTMLElement) {
  const currentUser = getAuthUser()
  if (!currentUser || currentUser.rol !== 'Admin') {
    window.location.hash = '#/dashboard'
    return
  }

  root.innerHTML = `
    <main class="page page-admin">
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
            <h1>Administración de usuarios</h1>
          </div>
          <div id="header-controls" class="header-controls"></div>
        </div>
        <div class="admin-actions" style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:18px;">
          <button id="admin-add-user" class="button primary">Agregar usuario</button>
          <form id="admin-search-form" class="search-form" style="display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end;">
            <label>
              Buscar por
              <select id="admin-search-type" name="type">
                <option value="correo">Correo</option>
                <option value="id">ID</option>
              </select>
            </label>
            <label>
              Valor
              <input id="admin-search-value" name="value" placeholder="Correo o id" />
            </label>
            <button type="submit" class="button outline">Buscar</button>
            <button type="button" id="admin-search-clear" class="button small">Limpiar</button>
          </form>
        </div>
        <div id="admin-error" class="form-error"></div>
        <div id="admin-user-list"></div>
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
      <a href="#/classrooms" data-router class="nav-link">Classrooms</a>
      <a href="#/profile" data-router class="nav-link">Perfil</a>
      <a href="#/admin/users" data-router class="nav-link">Usuarios</a>
    `
  }

  const sidebarLogout = document.querySelector<HTMLButtonElement>('#sidebar-logout')
  const performLogout = () => {
    clearAuthStorage()
    window.location.hash = '#/login'
  }
  sidebarLogout?.addEventListener('click', performLogout)

  renderHeaderControls(getTheme())

  const addButton = document.querySelector<HTMLButtonElement>('#admin-add-user')
  const searchForm = document.querySelector<HTMLFormElement>('#admin-search-form')
  const clearButton = document.querySelector<HTMLButtonElement>('#admin-search-clear')

  addButton?.addEventListener('click', async () => {
    const values = await openUserFormModal('Agregar usuario')
    if (!values) return
    const result = await createUser(values)
    const error = document.querySelector<HTMLDivElement>('#admin-error')
    if (!result.ok) {
      if (error) error.textContent = result.error || 'No se pudo crear el usuario.'
      return
    }
    if (error) error.textContent = ''
    await loadUserList(root)
  })

  searchForm?.addEventListener('submit', async (event) => {
    event.preventDefault()
    const typeSelect = document.querySelector<HTMLSelectElement>('#admin-search-type')
    const valueInput = document.querySelector<HTMLInputElement>('#admin-search-value')
    if (!typeSelect || !valueInput) return

    const value = valueInput.value.trim()
    if (!value) {
      await loadUserList(root)
      return
    }

    const filter = typeSelect.value === 'id' ? { id: Number(value) } : { correo: value }
    await loadUserList(root, filter)
  })

  clearButton?.addEventListener('click', async () => {
    const valueInput = document.querySelector<HTMLInputElement>('#admin-search-value')
    if (valueInput) valueInput.value = ''
    await loadUserList(root)
  })

  await loadUserList(root)
}
