import { getAuthUser, getTheme, clearAuthStorage } from '../hooks/useLocalStorage'
import { renderHeaderControls } from '../app'
import { getUserClassrooms } from '../services/classroomService'

export async function renderDashboardPage(root: HTMLElement) {
  const currentUser = getAuthUser()
  const fullName = currentUser ? `${currentUser.nombre} ${currentUser.apellido}` : 'Usuario'

  const classroomsResult = await getUserClassrooms()
  const coursesList: string[] = classroomsResult.ok ? (classroomsResult.data ?? []).map((classroom) => classroom.nombre) : []
  const coursesActive = classroomsResult.ok ? coursesList.length : 0
  const activity = { weekly: 0, monthly: 0, annual: 0 }

  root.innerHTML = `
    <main class="page page-dashboard">
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
          <div style="display:flex;align-items:center;gap:12px;">
            <button id="nav-toggle" class="nav-toggle" aria-label="Abrir menú">☰</button>
            <span class="brand">Acadelytics</span>
            <h1 class="dashboard-title">¡Bienvenido, ${fullName}!</h1>
          </div>
          <div style="display:flex;align-items:center;gap:12px;">
            <div id="header-controls" class="header-controls"></div>
          </div>
        </div>

        <section class="overview-grid">
          <article class="stat-card">
            <div class="stat-label">MIS CURSOS ACTIVOS</div>
            <div class="stat-value">${coursesActive}</div>
            <div class="stat-list">
              ${coursesList.length === 0 ? '<p>No pertenece a ningún curso</p>' : `<ul>${coursesList.map(c=>`<li>${c}</li>`).join('')}</ul>`}
            </div>
          </article>

          <article class="stat-card">
            <div class="stat-label">Actividad</div>
            <div class="activity-tabs">
              <button class="tab active" data-target="weekly">Actividad Semanal</button>
              <button class="tab" data-target="monthly">Actividad Mensual</button>
              <button class="tab" data-target="annual">Actividad Anual</button>
            </div>
            <div class="activity-counts">
              <div>Semanal: ${activity.weekly}</div>
              <div>Mensual: ${activity.monthly}</div>
              <div>Anual: ${activity.annual}</div>
            </div>
          </article>
        </section>

        <section class="charts-grid">
          <div class="chart-card">
            <h3>Tiempo de uso</h3>
            <div class="chart-content">
              <div class="chart-placeholder">No ha habido actividad</div>
            </div>
          </div>

          <div class="chart-card">
            <h3>Distribución de Tiempo por Categoría</h3>
            <div class="chart-content">
              <div class="chart-placeholder">No ha habido actividad</div>
            </div>
          </div>
        </section>
      </section>
    </main>
  `

  const navToggle = document.querySelector<HTMLButtonElement>('#nav-toggle')
  const sidebarClose = document.querySelector<HTMLButtonElement>('#sidebar-close')
  navToggle?.addEventListener('click', () => {
    document.body.classList.add('sidebar-open')
  })
  sidebarClose?.addEventListener('click', () => {
    document.body.classList.remove('sidebar-open')
  })
  const sidebarNav = document.querySelector<HTMLDivElement>('.sidebar-nav')
  if (sidebarNav) {
    sidebarNav.innerHTML = `
      <a href="#/dashboard" data-router class="nav-link">Inicio</a>
      <a href="#/classrooms" data-router class="nav-link">Classrooms</a>
      <a href="#/profile" data-router class="nav-link">Perfil</a>
      ${currentUser?.rol === 'Admin' ? '<a href="#/admin/users" data-router class="nav-link">Usuarios</a>' : ''}
    `
  }

  const sidebarLogout = document.querySelector<HTMLButtonElement>('#sidebar-logout')
  sidebarLogout?.addEventListener('click', () => {
    clearAuthStorage()
    window.location.hash = '#/login'
  })

  const tabs = Array.from(document.querySelectorAll<HTMLButtonElement>('.activity-tabs .tab'))
  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'))
      tab.classList.add('active')
    })
  })

  renderHeaderControls(getTheme())
}
