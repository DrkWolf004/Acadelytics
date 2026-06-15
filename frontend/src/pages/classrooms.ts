import { getAuthUser, getTheme } from '../hooks/useLocalStorage'
import { renderHeaderControls } from '../app'
import { showConfirmationPopup } from '../modal'
import { createFileUploadUI } from '../fileUpload'
import {
  addClassroomMember,
  createClassroom,
  deleteClassroom,
  getClassroomMembers,
  getUserClassrooms,
  updateClassroom,
} from '../services/classroomService'
import { deleteFile, getFilesByClassFolder, updateFile } from '../services/fileService'
import type { Classroom, ClassroomMember, FileRecord } from '../types'

function createModal(innerHtml: string, onClose: () => void): HTMLDivElement {
  const overlay = document.createElement('div')
  overlay.className = 'modal-overlay'
  overlay.innerHTML = `
    <div class="modal-dialog">
      ${innerHtml}
    </div>
  `
  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) {
      onClose()
    }
  })
  overlay.querySelector<HTMLDivElement>('.modal-dialog')?.addEventListener('click', (event) => event.stopPropagation())
  document.body.appendChild(overlay)
  return overlay
}

function closeModal(modal: HTMLDivElement) {
  if (document.body.contains(modal)) {
    document.body.removeChild(modal)
  }
}

function renderClassroomCard(classroom: Classroom, currentRole: string | undefined) {
  const card = document.createElement('article')
  card.className = 'classroom-card'
  card.innerHTML = `
    <div class="card-header">
      <div>
        <p class="card-type">${classroom.type}</p>
        <h2>${classroom.nombre}</h2>
      </div>
      <button class="button outline small classroom-actions-button" data-classroom-id="${classroom.id}">Acciones</button>
    </div>
    <div class="card-meta">
      <span>Creado: ${new Date(classroom.create_at).toLocaleDateString()}</span>
    </div>
  `

  const actionsButton = card.querySelector<HTMLButtonElement>('.classroom-actions-button')
  actionsButton?.addEventListener('click', () => showClassroomActions(classroom, currentRole))
  return card
}

function renderClassroomList(classrooms: Classroom[], currentRole: string | undefined) {
  const container = document.querySelector<HTMLDivElement>('#classroom-list')
  if (!container) return
  container.innerHTML = ''
  if (classrooms.length === 0) {
    container.innerHTML = '<p class="empty-state">No tienes classrooms aún. Crea uno para comenzar.</p>'
    return
  }
  const grid = document.createElement('div')
  grid.className = 'classrooms-grid'
  classrooms.forEach((classroom) => {
    grid.appendChild(renderClassroomCard(classroom, currentRole))
  })
  container.appendChild(grid)
}

function renderMemberList(members: ClassroomMember[]) {
  if (members.length === 0) {
    return '<p>No hay miembros registrados en esta classroom.</p>'
  }
  return `
    <ul class="member-list">
      ${members
        .map(
          (member) => `
            <li>
              <strong>${member.nombre} ${member.apellido}</strong>
              <span>${member.correo}</span>
              <span>${member.rol}</span>
            </li>
          `,
        )
        .join('')}
    </ul>
  `
}

function renderFilesList(files: FileRecord[]) {
  if (files.length === 0) {
    return '<p class="empty-state">No hay archivos disponibles en esta carpeta.</p>'
  }
  return `
    <ul class="files-list">
      ${files
        .map(
          (file) => `
            <li class="file-item" data-file-id="${file.id}">
              <div class="file-info">
                <strong>${file.filename}</strong>
                <span class="file-date">${new Date(file.upload_at).toLocaleDateString()}</span>
              </div>
              <div class="file-actions">
                <button class="button small outline edit-file-btn" data-file-id="${file.id}">Editar</button>
                <button class="button small danger delete-file-btn" data-file-id="${file.id}">Eliminar</button>
              </div>
            </li>
          `,
        )
        .join('')}
    </ul>
  `
}

async function showFilesModal(classroom: Classroom) {
  if (!classroom.class_folder_id) {
    alert('Esta classroom no tiene una carpeta asignada.')
    return
  }

  const filesResult = await getFilesByClassFolder(classroom.class_folder_id)
  if (!filesResult.ok) {
    alert(filesResult.error || 'No se pudieron cargar los archivos.')
    return
  }

  let files = filesResult.data ?? []

  const filesModal = createModal(
    `
      <div class="modal-header">
        <h2>Archivos de ${classroom.nombre}</h2>
      </div>
      <div class="modal-content files-modal-content">
        <div id="upload-container"></div>
        <div class="files-list-section" id="files-list-section">
          ${renderFilesList(files)}
        </div>
      </div>
    `,
    () => closeModal(filesModal),
  )

  const uploadContainer = filesModal.querySelector<HTMLDivElement>('#upload-container')
  if (uploadContainer) {
    const uploadUI = await createFileUploadUI(classroom.class_folder_id, async (updatedFiles) => {
      files = updatedFiles
      const filesListSection = filesModal.querySelector<HTMLDivElement>('#files-list-section')
      if (filesListSection) {
        filesListSection.innerHTML = renderFilesList(updatedFiles)
        attachFileListeners(filesModal, classroom, files)
      }
    })
    uploadContainer.appendChild(uploadUI)
  }

  attachFileListeners(filesModal, classroom, files)
}

function attachFileListeners(modal: HTMLDivElement, classroom: Classroom, files: FileRecord[]) {
  modal.querySelectorAll<HTMLButtonElement>('.edit-file-btn').forEach((btn) => {
    btn.addEventListener('click', async (event) => {
      const fileId = parseInt((event.target as HTMLButtonElement).dataset.fileId || '0')
      const fileItem = files.find((f) => f.id === fileId)
      if (!fileItem) return

      const editFileModal = createModal(
        `
          <div class="modal-header">
            <h2>Editar archivo</h2>
          </div>
          <form id="edit-file-form" class="modal-form">
            <label>
              Nombre del archivo
              <input name="filename" value="${fileItem.filename}" required />
            </label>
            <div class="modal-form-actions">
              <button class="button primary" type="submit">Guardar</button>
            </div>
          </form>
        `,
        () => closeModal(editFileModal),
      )

      const form = editFileModal.querySelector<HTMLFormElement>('#edit-file-form')
      form?.addEventListener('submit', async (submitEvent) => {
        submitEvent.preventDefault()
        const formData = new FormData(form)
        const filename = formData.get('filename')?.toString().trim() || ''
        if (!filename) return

        const result = await updateFile(fileId, { filename })
        if (!result.ok) {
          alert(result.error || 'No se pudo actualizar el archivo.')
          return
        }
        closeModal(editFileModal)
        closeModal(modal)
        await showFilesModal(classroom)
      })
    })
  })

  modal.querySelectorAll<HTMLButtonElement>('.delete-file-btn').forEach((btn) => {
    btn.addEventListener('click', async (event) => {
      const fileId = parseInt((event.target as HTMLButtonElement).dataset.fileId || '0')
      const confirmed = await showConfirmationPopup('¿Eliminar este archivo?', 'Eliminar archivo')
      if (!confirmed) return

      const result = await deleteFile(fileId)
      if (!result.ok) {
        alert(result.error || 'No se pudo eliminar el archivo.')
        return
      }
      closeModal(modal)
      await showFilesModal(classroom)
    })
  })
}

async function showClassroomActions(classroom: Classroom, currentRole: string | undefined) {
  const addMemberButton = currentRole === 'Profesor' || currentRole === 'Admin'
    ? classroom.type === 'Grupal'
      ? '<button class="button outline" id="add-member">Agregar miembro</button>'
      : ''
    : ''

  const canDelete = currentRole === 'Profesor' || currentRole === 'Admin' || (currentRole === 'Alumno' && classroom.type === 'Solitario')

  const canEdit = currentRole === 'Profesor' || currentRole === 'Admin' || (currentRole === 'Alumno' && classroom.type === 'Solitario')

  const modal = createModal(
    `
      <div class="modal-header">
        <h2>${classroom.nombre}</h2>
      </div>
      <div class="modal-content">
        <p><strong>Tipo:</strong> ${classroom.type}</p>
        <div class="modal-actions">
          <button class="button primary" id="view-folder">Ver carpeta</button>
          <button class="button outline" id="view-members">Ver miembros</button>
          ${addMemberButton}
          ${canEdit ? '<button class="button outline" id="edit-classroom">Editar classroom</button>' : ''}
          ${canDelete ? '<button class="button danger" id="delete-classroom">Eliminar classroom</button>' : ''}
        </div>
      </div>
    `,
    () => closeModal(modal),
  )

  modal.querySelector<HTMLButtonElement>('#view-folder')?.addEventListener('click', () => {
    closeModal(modal)
    showFilesModal(classroom)
  })

  modal.querySelector<HTMLButtonElement>('#view-members')?.addEventListener('click', async () => {
    const membersResult = await getClassroomMembers(classroom.id)
    if (!membersResult.ok) {
      alert(membersResult.error || 'No se pudieron cargar los miembros.')
      return
    }

    const membersModal = createModal(
      `
        <div class="modal-header">
          <h2>Miembros de ${classroom.nombre}</h2>
        </div>
        <div class="modal-content">
          ${renderMemberList(membersResult.data ?? [])}
        </div>
      `,
      () => closeModal(membersModal),
    )
  })

  if (classroom.type === 'Grupal') {
    modal.querySelector<HTMLButtonElement>('#add-member')?.addEventListener('click', async () => {
      const addModal = createModal(
        `
          <div class="modal-header">
            <h2>Agregar miembro</h2>
          </div>
          <form id="add-member-form" class="modal-form">
            <label>
              Correo del alumno
              <input type="email" name="correo" required />
            </label>
            <div class="modal-form-actions">
              <button class="button primary" type="submit">Agregar</button>
            </div>
          </form>
        `,
        () => closeModal(addModal),
      )

      const form = addModal.querySelector<HTMLFormElement>('#add-member-form')
      form?.addEventListener('submit', async (event) => {
        event.preventDefault()
        const formData = new FormData(form)
        const correo = formData.get('correo')?.toString().trim() || ''
        if (!correo) return

        const result = await addClassroomMember(classroom.id, correo)
        if (!result.ok) {
          alert(result.error || 'No se pudo agregar el usuario.')
          return
        }
        closeModal(addModal)
        closeModal(modal)
        await refreshClassrooms()
        alert('Miembro agregado correctamente.')
      })
    })
  }

  modal.querySelector<HTMLButtonElement>('#edit-classroom')?.addEventListener('click', () => {
    const editModal = createModal(
      `
        <div class="modal-header">
          <h2>Editar classroom</h2>
        </div>
        <form id="edit-classroom-form" class="modal-form">
          <label>
            Nombre
            <input name="nombre" value="${classroom.nombre}" required />
          </label>
          ${currentRole === 'Alumno' ? `
            <input type="hidden" name="type" value="${classroom.type}" />
          ` : `
            <label>
              Tipo
              <select name="type" required>
                <option value="Solitario" ${classroom.type === 'Solitario' ? 'selected' : ''}>Solitario</option>
                <option value="Grupal" ${classroom.type === 'Grupal' ? 'selected' : ''}>Grupal</option>
              </select>
            </label>
          `}
          <div class="modal-form-actions">
            <button class="button primary" type="submit">Guardar</button>
          </div>
        </form>
      `,
      () => closeModal(editModal),
    )

    const form = editModal.querySelector<HTMLFormElement>('#edit-classroom-form')
    form?.addEventListener('submit', async (event) => {
      event.preventDefault()
      const formData = new FormData(form)
      const nombre = formData.get('nombre')?.toString().trim() || ''
      const type = formData.get('type')?.toString().trim() || 'Solitario'
      if (!nombre) return

      const result = await updateClassroom(classroom.id, { nombre, type })
      if (!result.ok) {
        alert(result.error || 'No se pudo actualizar la classroom.')
        return
      }
      closeModal(editModal)
      closeModal(modal)
      await refreshClassrooms()
      alert('Classroom actualizada correctamente.')
    })
  })

  modal.querySelector<HTMLButtonElement>('#delete-classroom')?.addEventListener('click', async () => {
    const confirmed = await showConfirmationPopup('¿Eliminar esta classroom? Esta acción no se puede deshacer.', 'Eliminar classroom')
    if (!confirmed) return

    const result = await deleteClassroom(classroom.id)
    if (!result.ok) {
      alert(result.error || 'No se pudo eliminar la classroom.')
      return
    }
    closeModal(modal)
    await refreshClassrooms()
    alert('Classroom eliminada correctamente.')
  })
}

async function refreshClassrooms() {
  const currentUser = getAuthUser()
  const listError = document.querySelector<HTMLDivElement>('#classroom-error')
  if (!listError) return
  listError.textContent = ''

  const result = await getUserClassrooms()
  if (!result.ok) {
    listError.textContent = result.error || 'No se pudieron obtener las classrooms.'
    return
  }

  renderClassroomList(result.data ?? [], currentUser?.rol)
}

function openCreateClassroomModal(currentRole: string, messageContainer: HTMLDivElement | null, errorContainer: HTMLDivElement | null) {
  if (messageContainer) {
    messageContainer.textContent = ''
  }
  if (errorContainer) {
    errorContainer.textContent = ''
  }

  const modal = createModal(
    `
      <div class="modal-header">
        <h2>Crear classroom</h2>
      </div>
      <form id="create-classroom-form" class="modal-form">
        <label>
          Nombre
          <input name="nombre" required />
        </label>
        <label>
          Tipo
          <select name="type" required>
            <option value="Solitario">Solitario</option>
            ${currentRole !== 'Alumno' ? '<option value="Grupal">Grupal</option>' : ''}
          </select>
        </label>
        <div class="modal-form-actions">
          <button type="submit" class="button primary">Crear</button>
        </div>
      </form>
    `,
    () => closeModal(modal),
  )

  const form = modal.querySelector<HTMLFormElement>('#create-classroom-form')
  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    const formData = new FormData(form)
    const nombre = formData.get('nombre')?.toString().trim() || ''
    const type = formData.get('type')?.toString().trim() || 'Solitario'

    if (!nombre) return

    if (currentRole === 'Alumno' && type !== 'Solitario') {
      alert('Los alumnos solo pueden crear classrooms solitarios.')
      return
    }

    const result = await createClassroom({ nombre, type })
    if (!result.ok) {
      if (errorContainer) {
        errorContainer.textContent = result.error || 'No se pudo crear la classroom.'
      }
      return
    }

    if (messageContainer) {
      messageContainer.textContent = 'Classroom creada correctamente.'
    }
    if (errorContainer) {
      errorContainer.textContent = ''
    }
    closeModal(modal)
    await refreshClassrooms()
  })
}

export async function renderClassroomsPage(root: HTMLElement) {
  const currentUser = getAuthUser()
  if (!currentUser) {
    window.location.hash = '#/login'
    return
  }

  root.innerHTML = `
    <main class="page page-classrooms">
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

      <section class="dashboard-card dashboard-main">
        <div class="dashboard-header">
          <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
            <button id="nav-toggle" class="nav-toggle" aria-label="Abrir menú">☰</button>
            <div>
              <span class="brand">Acadelytics</span>
              <h1 class="dashboard-title">Classrooms</h1>
            </div>
          </div>
          <div id="header-controls" class="header-controls"></div>
        </div>

        <section class="classroom-create-card">
          <div class="section-header">
            <h2>Crear nueva classroom</h2>
            <button id="open-create-classroom" class="button primary">Nueva classroom</button>
          </div>
          <div id="classroom-create-message" class="form-success"></div>
          <div id="classroom-create-error" class="form-error"></div>
        </section>

        <section class="classroom-list-section">
          <div class="section-header">
            <h2>Mis classrooms</h2>
          </div>
          <div id="classroom-error" class="form-error"></div>
          <div id="classroom-list"></div>
        </section>
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
      <a href="#/classrooms" data-router class="nav-link active">Classrooms</a>
      <a href="#/profile" data-router class="nav-link">Perfil</a>
      ${currentUser.rol === 'Admin' ? '<a href="#/admin/users" data-router class="nav-link">Usuarios</a>' : ''}
    `
  }

  const sidebarLogout = document.querySelector<HTMLButtonElement>('#sidebar-logout')
  sidebarLogout?.addEventListener('click', () => {
    localStorage.removeItem('acadelytics_token')
    localStorage.removeItem('acadelytics_user')
    window.location.hash = '#/login'
  })

  const createButton = document.querySelector<HTMLButtonElement>('#open-create-classroom')
  const createMessage = document.querySelector<HTMLDivElement>('#classroom-create-message')
  const createError = document.querySelector<HTMLDivElement>('#classroom-create-error')

  createButton?.addEventListener('click', () => {
    openCreateClassroomModal(currentUser.rol, createMessage, createError)
  })

  await refreshClassrooms()
  renderHeaderControls(getTheme())
}
