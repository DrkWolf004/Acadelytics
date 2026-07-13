import { getAuthUser } from '../hooks/useLocalStorage'
import { createModal, closeModal } from '../modal'
import {
  createHomework,
  deleteHomework,
  downloadHomeworkAttachment,
  downloadHomeworkResponseFile,
  getHomeworks,
  submitHomeworkResponse,
  updateHomework,
  getHomeworkResponses,
  gradeHomeworkResponse,
  autoGradeMissingResponses,
} from '../services/homeworkService'
import type { Classroom, Homework } from '../types'

function formatDeadline(value: string) {
  return new Date(value).toLocaleString('es-ES', {
    dateStyle: 'short',
    timeStyle: 'short',
  })
}

function getBadgeClass(status: string) {
  switch (status) {
    case 'received':
      return 'received'
    case 'qualified':
      return 'qualified'
    default:
      return 'pending'
  }
}

function getBadgeLabel(status: string) {
  switch (status) {
    case 'received':
      return 'Recibida'
    case 'qualified':
      return 'Calificada'
    default:
      return 'Pendiente'
  }
}

function getGradeClass(grade?: string | null) {
  if (!grade) return ''
  const numeric = parseFloat(grade)
  return numeric < 4 ? 'low' : 'high'
}

function renderHomeworkList(homeworks: Homework[], currentRole: string | undefined, classroom: Classroom, refresh: () => Promise<void>) {
  const container = document.createElement('div')
  container.className = 'homework-modal-content'
  container.innerHTML = `
    <div class="homework-filters">
      <button class="homework-filter-btn active" data-filter="all">Todas</button>
      <button class="homework-filter-btn" data-filter="pending">Pendiente</button>
      <button class="homework-filter-btn" data-filter="received">Recibida</button>
      <button class="homework-filter-btn" data-filter="qualified">Calificada</button>
    </div>
    <ul class="homework-list"></ul>
  `

  const list = container.querySelector<HTMLUListElement>('.homework-list')
  const applyFilter = (filter: string) => {
    const items = list?.querySelectorAll<HTMLLIElement>('.homework-item') ?? []
    items.forEach((item) => {
      const matches = filter === 'all' || item.dataset.status === filter
      item.style.display = matches ? '' : 'none'
    })
  }

  container.querySelectorAll<HTMLButtonElement>('.homework-filter-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      container.querySelectorAll('.homework-filter-btn').forEach((button) => button.classList.remove('active'))
      btn.classList.add('active')
      applyFilter(btn.dataset.filter || 'all')
    })
  })

  const items = homeworks.map((homework) => {
    const canManage = currentRole === 'Profesor'
    const canRespond = currentRole === 'Alumno' && new Date(homework.deadline_at) > new Date()
    const actions = []
    if (canManage) {
      actions.push(`<button class="button small outline grade-homework-btn" data-homework-id="${homework.id}">Calificar</button>`)
      actions.push(`<button class="button small outline edit-homework-btn" data-homework-id="${homework.id}">Editar</button>`)
      actions.push(`<button class="button small danger delete-homework-btn" data-homework-id="${homework.id}">Eliminar</button>`)
    }
    actions.push(`<button class="button small primary open-homework-btn" data-homework-id="${homework.id}">Examinar</button>`)
    if (canRespond) {
      actions.push(`<button class="button small outline respond-homework-btn" data-homework-id="${homework.id}">Responder</button>`)
    }
    return `
      <li class="homework-item" data-status="${homework.student_status}">
        <div class="homework-item-header">
          <div>
            <h3>${homework.title}</h3>
            <p>${homework.description || 'Sin descripción'}</p>
            <p class="file-date">Vence: ${formatDeadline(homework.deadline_at)}</p>
          </div>
          <span class="homework-badge ${getBadgeClass(homework.student_status)}">${getBadgeLabel(homework.student_status)}</span>
        </div>
        ${homework.response?.grade ? `<p class="homework-grade ${getGradeClass(homework.response.grade)}">Nota: ${homework.response.grade}</p>` : ''}
        <div class="homework-actions">
          ${actions.join('')}
        </div>
      </li>
    `
  }).join('')

  if (list) list.innerHTML = items
  attachHomeworkActions(container, classroom, refresh)
  return container
}

function attachHomeworkActions(container: HTMLElement, classroom: Classroom, refresh: () => Promise<void>) {
  container.querySelectorAll<HTMLButtonElement>('.open-homework-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const homeworkId = Number(btn.dataset.homeworkId)
      const homeworks = await getHomeworks(classroom.id)
      if (!homeworks.ok) {
        alert(homeworks.error || 'No se pudieron cargar las tareas')
        return
      }
      const homework = homeworks.data?.find((item) => item.id === homeworkId)
      if (!homework) return
      openHomeworkDetailModal(homework, refresh)
    })
  })

  container.querySelectorAll<HTMLButtonElement>('.respond-homework-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const homeworkId = Number(btn.dataset.homeworkId)
      const homeworks = await getHomeworks(classroom.id)
      if (!homeworks.ok) {
        alert(homeworks.error || 'No se pudieron cargar las tareas')
        return
      }
      const homework = homeworks.data?.find((item) => item.id === homeworkId)
      if (!homework) return
      openResponseModal(homework, refresh)
    })
  })

  container.querySelectorAll<HTMLButtonElement>('.edit-homework-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const homeworkId = Number(btn.dataset.homeworkId)
      const homeworks = await getHomeworks(classroom.id)
      if (!homeworks.ok) {
        alert(homeworks.error || 'No se pudieron cargar las tareas')
        return
      }
      const homework = homeworks.data?.find((item) => item.id === homeworkId)
      if (!homework) return
      openHomeworkFormModal(classroom, homework)
    })
  })

  container.querySelectorAll<HTMLButtonElement>('.delete-homework-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const confirmed = window.confirm('¿Eliminar esta tarea?')
      if (!confirmed) return
      const homeworkId = Number(btn.dataset.homeworkId)
      const result = await deleteHomework(homeworkId)
      if (!result.ok) {
        alert(result.error || 'No se pudo eliminar la tarea')
        return
      }
      await refresh()
    })
  })

  container.querySelectorAll<HTMLButtonElement>('.grade-homework-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const homeworkId = Number(btn.dataset.homeworkId)
      const homeworks = await getHomeworks(classroom.id)
      if (!homeworks.ok) {
        alert(homeworks.error || 'No se pudieron cargar las tareas')
        return
      }
      const homework = homeworks.data?.find((item) => item.id === homeworkId)
      if (!homework) return
      openGradingPanel(homework, refresh)
    })
  })
}

function openHomeworkDetailModal(homework: Homework, refresh: () => Promise<void>) {
  const modal = createModal(`
    <div class="modal-header">
      <h2>${homework.title}</h2>
    </div>
    <div class="modal-content homework-modal-content">
      <div class="homework-detail-card">
        <p><strong>Descripción:</strong> ${homework.description || 'Sin descripción'}</p>
        <p><strong>Fecha límite:</strong> ${formatDeadline(homework.deadline_at)}</p>
      </div>
      ${homework.attached_file_id ? `<div class="homework-actions"><button class="button outline small" id="download-attachment">📥 Descargar archivo de la tarea</button></div>` : ''}
      ${homework.response ? `
        <div class="homework-detail-card">
          <h3>Tu respuesta</h3>
          <p><strong>Fecha de envío:</strong> ${formatDeadline(homework.response.submitted_at)}</p>
          ${homework.response.explanation ? `<p><strong>Tu explicación:</strong> ${homework.response.explanation}</p>` : ''}
          ${homework.response.filename ? `<p><strong>Archivo:</strong> ${homework.response.filename}</p>` : ''}
          ${homework.response.filename && homework.response.id ? `<div class="homework-actions"><button class="button outline small" id="download-response">📥 Descargar tu respuesta</button></div>` : ''}
          ${homework.response.grade ? `<p><strong>Calificación:</strong> <span class="homework-grade ${getGradeClass(homework.response.grade)}">${homework.response.grade}</span></p>` : ''}
        </div>
      ` : `
        <div class="homework-detail-card">
          <h3>Responder tarea</h3>
          <form id="homework-response-form" class="homework-response-form">
            <textarea name="explanation" placeholder="Escribe tu respuesta aquí" rows="6"></textarea>
            <label>
              Archivo adjunto
              <input type="file" name="file" />
            </label>
            <div class="homework-actions">
              <button class="button primary" type="submit">Guardar respuesta</button>
            </div>
          </form>
        </div>
      `}
    </div>
  `, () => closeModal(modal))

  const form = modal.querySelector<HTMLFormElement>('#homework-response-form')
  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    const formData = new FormData(form)
    const explanation = formData.get('explanation')?.toString().trim() || ''
    const file = formData.get('file') as File | null
    const result = await submitHomeworkResponse(homework.id, { explanation }, file || undefined)
    if (!result.ok) {
      alert(result.error || 'No se pudo enviar la respuesta')
      return
    }
    await refresh()
    closeModal(modal)
  })

  modal.querySelector<HTMLButtonElement>('#download-attachment')?.addEventListener('click', async () => {
    const result = await downloadHomeworkAttachment(homework.id)
    if (!result.ok) {
      alert(result.error || 'No se pudo descargar el archivo')
      return
    }
    const url = URL.createObjectURL(result.data!)
    const link = document.createElement('a')
    link.href = url
    link.download = `tarea-${homework.id}`
    link.click()
    URL.revokeObjectURL(url)
  })

  modal.querySelector<HTMLButtonElement>('#download-response')?.addEventListener('click', async () => {
    const result = await downloadHomeworkResponseFile(homework.id, homework.response!.id)
    if (!result.ok) {
      alert(result.error || 'No se pudo descargar el archivo')
      return
    }
    const url = URL.createObjectURL(result.data!)
    const link = document.createElement('a')
    link.href = url
    link.download = homework.response!.filename || `respuesta-${homework.response!.id}`
    link.click()
    URL.revokeObjectURL(url)
  })
}

function openResponseModal(homework: Homework, refresh: () => Promise<void>) {
  const modal = createModal(`
    <div class="modal-header">
      <h2>Responder ${homework.title}</h2>
    </div>
    <div class="modal-content">
      <form id="response-form" class="homework-response-form">
        <textarea name="explanation" placeholder="Escribe tu respuesta aquí" rows="6"></textarea>
        <label>
          Archivo adjunto
          <input type="file" name="file" />
        </label>
        <div class="homework-actions">
          <button class="button primary" type="submit">Enviar respuesta</button>
        </div>
      </form>
    </div>
  `, () => closeModal(modal))

  const form = modal.querySelector<HTMLFormElement>('#response-form')
  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    const formData = new FormData(form)
    const explanation = formData.get('explanation')?.toString().trim() || ''
    const file = formData.get('file') as File | null
    const result = await submitHomeworkResponse(homework.id, { explanation }, file || undefined)
    if (!result.ok) {
      alert(result.error || 'No se pudo enviar la respuesta')
      return
    }
    await refresh()
    closeModal(modal)
  })
}

async function openGradingPanel(homework: Homework, refresh: () => Promise<void>) {
  const responses = await getHomeworkResponses(homework.id)
  if (!responses.ok) {
    alert(responses.error || 'No se pudieron cargar las respuestas')
    return
  }

  const isPastDeadline = new Date(homework.deadline_at) < new Date()
  const responsesList = responses.data || []

  const modal = createModal(`
    <div class="modal-header">
      <h2>Calificar: ${homework.title}</h2>
    </div>
    <div class="modal-content homework-modal-content">
      ${isPastDeadline ? '<p style="color: orange;">El plazo ha pasado. Puedes auto-calificar a quienes no respondieron.</p>' : ''}
      <table style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr style="border-bottom: 1px solid var(--border);">
            <th style="text-align: left; padding: 8px;">Alumno</th>
            <th style="text-align: center; padding: 8px;">Entregó</th>
            <th style="text-align: center; padding: 8px;">Nota</th>
            <th style="text-align: center; padding: 8px;">Archivo</th>
            <th style="text-align: center; padding: 8px;">Acciones</th>
          </tr>
        </thead>
        <tbody>
          ${responsesList.map(resp => `
            <tr style="border-bottom: 1px solid var(--border);">
              <td style="padding: 8px;">
                <div><strong>${resp.student_name}</strong></div>
                <div style="font-size: 0.9em; color: var(--muted);">${resp.student_email}</div>
              </td>
              <td style="text-align: center; padding: 8px;">
                ${resp.submitted ? '<span style="color: green;">✓ Sí</span>' : '<span style="color: red;">✗ No</span>'}
              </td>
              <td style="text-align: center; padding: 8px;">
                ${resp.grade ? `<span class="homework-grade ${getGradeClass(resp.grade)}">${resp.grade}</span>` : '-'}
              </td>
              <td style="text-align: center; padding: 8px;">
                ${resp.submitted && resp.filename ? `<button class="button small outline download-response-btn" data-response-id="${resp.response_id}" title="${resp.filename}">Descargar</button>` : '-'}
              </td>
              <td style="text-align: center; padding: 8px;">
                ${resp.submitted ? `<button class="button small outline grade-btn" data-response-id="${resp.response_id}">Calificar</button>` : '-'}
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      ${isPastDeadline ? `<div class="homework-actions"><button class="button outline" id="auto-grade-btn">Auto-calificar no entregados con 1</button></div>` : ''}
    </div>
  `, () => closeModal(modal))

  modal.querySelectorAll<HTMLButtonElement>('.download-response-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const responseId = Number(btn.dataset.responseId)
      const result = await downloadHomeworkResponseFile(homework.id, responseId)
      if (!result.ok) {
        alert('No se pudo descargar: ' + (result.error || 'Archivo no disponible'))
        return
      }
      const url = URL.createObjectURL(result.data!)
      const link = document.createElement('a')
      link.href = url
      link.download = btn.title || `respuesta-${responseId}`
      link.click()
      URL.revokeObjectURL(url)
    })
  })

  modal.querySelectorAll<HTMLButtonElement>('.grade-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const responseId = Number(btn.dataset.responseId)
      openGradeFormModal(homework.id, responseId, () => {
        closeModal(modal)
        void openGradingPanel(homework, refresh)
      })
    })
  })

  modal.querySelector<HTMLButtonElement>('#auto-grade-btn')?.addEventListener('click', async () => {
    const confirmed = window.confirm('¿Auto-calificar a todos los que no entregaron con nota 1?')
    if (!confirmed) return
    const result = await autoGradeMissingResponses(homework.id)
    if (!result.ok) {
      alert(result.error || 'No se pudo auto-calificar')
      return
    }
    alert('Calificación automática completada')
    await refresh()
    closeModal(modal)
  })
}

function openGradeFormModal(homeworkId: number, responseId: number, onClose: () => void) {
  const modal = createModal(`
    <div class="modal-header">
      <h2>Calificar respuesta</h2>
    </div>
    <div class="modal-content">
      <form id="grade-form" class="homework-response-form">
        <label>
          Nota (1.0 a 7.0)
          <input type="text" name="grade" placeholder="ej: 4.5" required />
        </label>
        <div class="homework-actions">
          <button class="button primary" type="submit">Guardar calificación</button>
        </div>
      </form>
    </div>
  `, () => closeModal(modal))

  const form = modal.querySelector<HTMLFormElement>('#grade-form')
  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    const formData = new FormData(form)
    const grade = formData.get('grade')?.toString().trim() || ''
    if (!grade) {
      alert('Completa la nota')
      return
    }
    const result = await gradeHomeworkResponse(homeworkId, responseId, grade)
    if (!result.ok) {
      alert(result.error || 'No se pudo calificar')
      return
    }
    alert('Calificación guardada correctamente')
    closeModal(modal)
    onClose()
  })
}

function openHomeworkFormModal(classroom: Classroom, homework?: Homework) {
  const modal = createModal(`
    <div class="modal-header">
      <h2>${homework ? 'Editar tarea' : 'Publicar tarea'}</h2>
    </div>
    <div class="modal-content">
      <form id="homework-form" class="homework-response-form">
        <label>
          Título
          <input type="text" name="title" value="${homework?.title || ''}" required />
        </label>
        <label>
          Descripción
          <textarea name="description" rows="4">${homework?.description || ''}</textarea>
        </label>
        <label>
          Fecha límite
          <input type="date" name="deadline_date" value="${homework?.deadline_at ? homework.deadline_at.split('T')[0] : ''}" required />
        </label>
        <label>
          Hora límite
          <input type="time" name="deadline_time" value="${homework?.deadline_at ? homework.deadline_at.substring(11, 16) : ''}" required />
        </label>
        <label>
          Archivo adjunto
          <input type="file" name="file" />
        </label>
        <div class="homework-actions">
          <button class="button primary" type="submit">Guardar</button>
        </div>
      </form>
    </div>
  `, () => closeModal(modal))

  const form = modal.querySelector<HTMLFormElement>('#homework-form')
  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    const formData = new FormData(form)
    const title = formData.get('title')?.toString().trim() || ''
    const description = formData.get('description')?.toString().trim() || ''
    const deadline_date = formData.get('deadline_date')?.toString().trim() || ''
    const deadline_time = formData.get('deadline_time')?.toString().trim() || ''
    const file = formData.get('file') as File | null
    if (!title || !deadline_date || !deadline_time) {
      alert('Completa el título, fecha y hora límite')
      return
    }

    const deadline_at = `${deadline_date}T${deadline_time}:00`
    const payload = { classroom_id: classroom.id, title, description, deadline_at }
    const result = homework
      ? await updateHomework(homework.id, payload, file || undefined)
      : await createHomework(payload, file || undefined)
    if (!result.ok) {
      alert(result.error || 'No se pudo guardar la tarea')
      return
    }
    closeModal(modal)
    window.location.reload()
  })
}

export async function openHomeworkModule(classroom: Classroom) {
  const currentUser = getAuthUser()
  if (!currentUser) return

  const modal = createModal(`
    <div class="modal-header">
      <h2>Tareas de ${classroom.nombre}</h2>
    </div>
    <div class="modal-content">
      <div class="homework-actions">
        ${currentUser.rol === 'Profesor' ? '<button class="button primary" id="create-homework">Publicar tarea</button>' : ''}
      </div>
      <div id="homework-list-container"></div>
    </div>
  `, () => closeModal(modal))

  const refresh = async () => {
    const result = await getHomeworks(classroom.id)
    if (!result.ok) {
      alert(result.error || 'No se pudieron cargar las tareas')
      return
    }
    const container = modal.querySelector<HTMLDivElement>('#homework-list-container')
    if (container) {
      container.innerHTML = ''
      container.appendChild(renderHomeworkList(result.data || [], currentUser.rol, classroom, refresh))
    }
  }

  modal.querySelector<HTMLButtonElement>('#create-homework')?.addEventListener('click', () => openHomeworkFormModal(classroom))
  await refresh()
}
