import { getAuthToken, getAuthUser, getTheme, clearAuthStorage } from '../hooks/useLocalStorage'
import { renderHeaderControls } from '../app'
import { deleteProfessorValidationRequest, getProfessorValidationRequests, reviewProfessorValidationRequest, submitProfessorValidation } from '../services/professorValidationService'
import { showConfirmationPopup } from '../modal'

function formatDate(dateString: string | null | undefined) {
  if (!dateString) return '-'
  try {
    const date = new Date(dateString)
    if (Number.isNaN(date.getTime())) return dateString
    return new Intl.DateTimeFormat('es-CL', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    }).format(date)
  } catch {
    return dateString
  }
}

function getFileLink(requestId: number, token?: string) {
  const baseUrl = `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/professor-validations/${requestId}/file`
  return token ? `${baseUrl}?token=${encodeURIComponent(token)}` : baseUrl
}

function renderRequestList(requests: Array<any>, isAdmin: boolean, currentUserId?: number, token?: string) {
  if (!requests.length) {
    return '<p>No hay solicitudes pendientes.</p>'
  }

  return `
    <div class="request-list">
      ${requests
        .map((request) => {
          const canViewFile = isAdmin || request.user_id === currentUserId
          return `
            <article class="request-card">
              <div class="request-card-header">
                <strong>${request.user?.nombre || 'Usuario'} ${request.user?.apellido || ''}</strong>
                <span class="badge">${request.status}</span>
              </div>
              <p><strong>Correo:</strong> ${request.user?.correo || '-'}</p>
              <p><strong>Archivo:</strong> ${request.filename}</p>
              ${canViewFile ? `<p><a href="${getFileLink(request.id, token)}" target="_blank" rel="noopener">Ver archivo</a></p>` : ''}
              <p><strong>Fecha:</strong> ${formatDate(request.create_at)}</p>
              ${request.review_comment ? `<p><strong>Comentario:</strong> ${request.review_comment}</p>` : ''}
              ${isAdmin ? `
                <div class="request-actions">
                  <button class="button secondary small view-file-button" data-request-id="${request.id}">Ver archivo</button>
                  <button class="button primary small approve-request" data-request-id="${request.id}">Aceptar</button>
                  <button class="button outline small reject-request" data-request-id="${request.id}">Rechazar</button>
                  <button class="button danger small delete-request" data-request-id="${request.id}">Eliminar</button>
                </div>
              ` : ''}
            </article>
          `
        })
        .join('')}
    </div>
  `
}

export async function renderProfessorValidationPage(root: HTMLElement) {
  const currentUser = getAuthUser()
  if (!currentUser) {
    window.location.hash = '#/login'
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
            <h1>Solicitudes de profesor</h1>
          </div>
          <div id="header-controls" class="header-controls"></div>
        </div>
        ${currentUser.rol === 'Admin' ? `
          <div class="admin-actions" style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:18px;">
            <button id="refresh-requests" class="button outline">Actualizar</button>
          </div>
        ` : `
          <form id="teacher-validation-form" class="auth-form">
            <label>
              Documento de validación
              <input type="file" name="document" accept=".pdf,.doc,.docx,.jpg,.jpeg,.png" required />
            </label>
            <button type="submit" class="button primary">Enviar solicitud</button>
          </form>
        `}
        <div id="professor-validation-message" class="form-success"></div>
        <div id="professor-validation-error" class="form-error"></div>
        <div id="professor-validation-list"></div>
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
      ${currentUser.rol === 'Admin' ? '<a href="#/admin/users" data-router class="nav-link">Usuarios</a>' : ''}
      ${currentUser.rol === 'Admin' ? '<a href="#/admin/professor-validations" data-router class="nav-link active">Solicitudes</a>' : ''}
    `
  }

  const sidebarLogout = document.querySelector<HTMLButtonElement>('#sidebar-logout')
  sidebarLogout?.addEventListener('click', () => {
    clearAuthStorage()
    window.location.hash = '#/login'
  })

  renderHeaderControls(getTheme())

  const listContainer = document.querySelector<HTMLDivElement>('#professor-validation-list')
  const message = document.querySelector<HTMLDivElement>('#professor-validation-message')
  const error = document.querySelector<HTMLDivElement>('#professor-validation-error')

  async function loadRequests() {
    if (!currentUser) return
    const result = await getProfessorValidationRequests(currentUser.rol === 'Admin' ? 'pendiente' : undefined)
    if (!result.ok) {
      if (error) error.textContent = result.error || 'No se pudieron cargar las solicitudes.'
      return
    }
    if (listContainer) {
      listContainer.innerHTML = renderRequestList(result.data || [], currentUser.rol === 'Admin', currentUser.id, getAuthToken() || undefined)
    }
    attachActions()
  }

  function attachActions() {
    const approveButtons = Array.from(document.querySelectorAll<HTMLButtonElement>('.approve-request'))
    approveButtons.forEach((button) => {
      button.addEventListener('click', async () => {
        const requestId = Number(button.dataset.requestId)
        const confirmed = await showConfirmationPopup('¿Aceptar esta solicitud de profesor?', 'Aceptar solicitud')
        if (!confirmed) return
        const result = await reviewProfessorValidationRequest(requestId, { status: 'aceptada' })
        if (!result.ok) {
          if (error) error.textContent = result.error || 'No se pudo aceptar la solicitud.'
          return
        }
        if (message) message.textContent = 'Solicitud aceptada.'
        await loadRequests()
      })
    })

    const rejectButtons = Array.from(document.querySelectorAll<HTMLButtonElement>('.reject-request'))
    rejectButtons.forEach((button) => {
      button.addEventListener('click', async () => {
        const requestId = Number(button.dataset.requestId)
        const confirmed = await showConfirmationPopup('¿Rechazar esta solicitud de profesor?', 'Rechazar solicitud')
        if (!confirmed) return
        const comment = window.prompt('Comentario de rechazo', 'No es un documento valido') || 'No es un documento valido'
        const result = await reviewProfessorValidationRequest(requestId, { status: 'rechazada', comment })
        if (!result.ok) {
          if (error) error.textContent = result.error || 'No se pudo rechazar la solicitud.'
          return
        }
        if (message) message.textContent = 'Solicitud rechazada.'
        await loadRequests()
      })
    })

    const viewButtons = Array.from(document.querySelectorAll<HTMLButtonElement>('.view-file-button'))
    viewButtons.forEach((button) => {
      button.addEventListener('click', () => {
        const requestId = Number(button.dataset.requestId)
        window.open(getFileLink(requestId, getAuthToken() || undefined), '_blank', 'noopener')
      })
    })

    const deleteButtons = Array.from(document.querySelectorAll<HTMLButtonElement>('.delete-request'))
    deleteButtons.forEach((button) => {
      button.addEventListener('click', async () => {
        const requestId = Number(button.dataset.requestId)
        const confirmed = await showConfirmationPopup('¿Eliminar esta solicitud?', 'Eliminar solicitud')
        if (!confirmed) return
        const result = await deleteProfessorValidationRequest(requestId)
        if (!result.ok) {
          if (error) error.textContent = result.error || 'No se pudo eliminar la solicitud.'
          return
        }
        await loadRequests()
      })
    })
  }

  const form = document.querySelector<HTMLFormElement>('#teacher-validation-form')
  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    const formData = new FormData(form)
    const file = formData.get('document') as File | null
    if (!file || !file.name) {
      if (error) error.textContent = 'Selecciona un archivo.'
      return
    }
    const result = await submitProfessorValidation(file)
    if (!result.ok) {
      if (error) error.textContent = result.error || 'No se pudo enviar la solicitud.'
      return
    }
    if (message) message.textContent = 'Solicitud enviada correctamente.'
    form.reset()
    await loadRequests()
  })

  const refreshButton = document.querySelector<HTMLButtonElement>('#refresh-requests')
  refreshButton?.addEventListener('click', () => loadRequests())

  await loadRequests()
}
