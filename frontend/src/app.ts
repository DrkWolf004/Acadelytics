import { renderDashboardPage } from './pages/dashboard'
import { renderHomePage } from './pages/home'
import { renderLoginPage } from './pages/login'
import { renderRegisterPage } from './pages/register'
import { renderProfilePage } from './pages/profile'
import { renderAdminPage } from './pages/admin'
import { getTheme, setTheme, getNotifications, removeNotification } from './hooks/useLocalStorage'

const root = document.querySelector<HTMLDivElement>('#app')!

const routes: Record<string, () => void> = {
  '': () => renderHomePage(root),
  '#/': () => renderHomePage(root),
  '#/login': () => renderLoginPage(root),
  '#/register': () => renderRegisterPage(root),
  '#/dashboard': () => renderDashboardPage(root),
  '#/profile': () => renderProfilePage(root),
  '#/admin/users': () => renderAdminPage(root),
}

function renderCurrentRoute() {
  const hash = window.location.hash || '#/'
  const route = routes[hash] ?? renderHomePage
  route()
  renderHeaderControls(getTheme())
}

function setupRouteLinks() {
  document.body.addEventListener('click', (event) => {
    const target = event.target as HTMLElement
    if (!target) return

    const anchor = target.closest('a[data-router]') as HTMLAnchorElement | null
    if (!anchor) return

    event.preventDefault()
    const href = anchor.getAttribute('href')
    if (!href) return
    window.location.hash = href
  })
}

function setupSidebarCloseOnOutsideClick() {
  document.body.addEventListener('click', (event) => {
    const sidebar = document.querySelector<HTMLElement>('.sidebar')
    const navToggle = document.querySelector<HTMLButtonElement>('#nav-toggle')
    if (!sidebar || !document.body.classList.contains('sidebar-open')) return

    const target = event.target as HTMLElement
    if (!target) return
    if (sidebar.contains(target) || navToggle?.contains(target)) return

    document.body.classList.remove('sidebar-open')
  })
}

window.addEventListener('hashchange', renderCurrentRoute)
window.addEventListener('load', () => {
  setupRouteLinks()
  setupSidebarCloseOnOutsideClick()
  renderCurrentRoute()
})

function buildNotificationsPanel(): HTMLElement {
  const panel = document.createElement('div')
  panel.className = 'notif-panel-content'

  const notifs = getNotifications()
  if (!notifs || notifs.length === 0) {
    const p = document.createElement('p')
    p.className = 'notif-empty'
    p.textContent = 'No tienes invitaciones a classrooms'
    panel.appendChild(p)
    return panel
  }

  const list = document.createElement('div')
  list.className = 'notif-list'
  notifs.forEach((n) => {
    const item = document.createElement('div')
    item.className = 'notif-item'

    const info = document.createElement('div')
    info.className = 'notif-info'
    info.innerHTML = `<strong>${n.inviterNombre} ${n.inviterApellido}</strong> te invitó a <em>${n.classroomName}</em>`

    const actions = document.createElement('div')
    actions.className = 'notif-actions'

    const accept = document.createElement('button')
    accept.className = 'button primary small'
    accept.textContent = '✓'
    accept.addEventListener('click', () => {
      removeNotification(n.id)
      refreshNotifPanel()
    })

    const reject = document.createElement('button')
    reject.className = 'button outline small'
    reject.textContent = '✕'
    reject.addEventListener('click', () => {
      removeNotification(n.id)
      refreshNotifPanel()
    })

    actions.appendChild(accept)
    actions.appendChild(reject)

    item.appendChild(info)
    item.appendChild(actions)
    list.appendChild(item)
  })

  panel.appendChild(list)
  return panel
}

function refreshNotifPanel() {
  const badge = document.querySelector<HTMLSpanElement>('.notif-badge')
  const panel = document.querySelector<HTMLDivElement>('#notif-panel')
  if (!badge || !panel) return

  const notifs = getNotifications()
  const count = notifs.length
  badge.textContent = count > 9 ? '10+' : String(count)
  badge.style.display = count === 0 ? 'none' : 'inline-flex'

  panel.innerHTML = ''
  const content = buildNotificationsPanel()
  panel.appendChild(content)
}

export function renderHeaderControls(currentTheme: 'light' | 'dark') {
  const container = document.querySelector<HTMLDivElement>('#header-controls')
  if (!container) return

  const isHomePage = ['', '#/', '#'].includes(window.location.hash)
  const showNotifications = !isHomePage

  container.innerHTML = `
    <div class="header-controls-inner">
      <div id="theme-switch" class="theme-switch" role="switch" aria-checked="${currentTheme === 'dark'}">
        <span class="icon icon-sun" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="5" />
            <line x1="12" y1="1" x2="12" y2="3" />
            <line x1="12" y1="21" x2="12" y2="23" />
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
            <line x1="1" y1="12" x2="3" y2="12" />
            <line x1="21" y1="12" x2="23" y2="12" />
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
          </svg>
        </span>
        <div class="switch-track"><div class="switch-dot"></div></div>
        <span class="icon icon-moon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12.79A9 9 0 1111.21 3a7 7 0 109.79 9.79z" />
          </svg>
        </span>
      </div>
      ${showNotifications ? `
      <div class="notif">
        <button id="notif-button" class="notif-btn" aria-expanded="false">
          <span class="icon icon-bell" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8a6 6 0 10-12 0c0 7-3 9-3 9h18s-3-2-3-9" />
              <path d="M13.73 21a2 2 0 01-3.46 0" />
            </svg>
          </span>
          <span class="notif-badge" style="display:none">0</span>
        </button>
        <div id="notif-panel" class="notif-panel hidden"></div>
      </div>
      ` : ''}
    </div>
  `

  const switchEl = document.querySelector<HTMLDivElement>('#theme-switch')
  const notifBtn = showNotifications ? document.querySelector<HTMLButtonElement>('#notif-button') : null
  const notifPanel = showNotifications ? document.querySelector<HTMLDivElement>('#notif-panel') : null

  switchEl?.addEventListener('click', () => {
    handleThemeToggle()
    renderHeaderControls(getTheme())
  })

  notifBtn?.addEventListener('click', (e) => {
    e.stopPropagation()
    if (!notifPanel) return
    const expanded = notifBtn.getAttribute('aria-expanded') === 'true'
    if (expanded) {
      notifPanel.classList.add('hidden')
      notifBtn.setAttribute('aria-expanded', 'false')
    } else {
      notifPanel.classList.remove('hidden')
      notifBtn.setAttribute('aria-expanded', 'true')
      refreshNotifPanel()
    }
  })

  document.addEventListener('click', (ev) => {
    const target = ev.target as HTMLElement
    if (!notifPanel || !notifBtn) return
    if (!notifPanel.contains(target) && target !== notifBtn) {
      notifPanel.classList.add('hidden')
      notifBtn.setAttribute('aria-expanded', 'false')
    }
  })

  refreshNotifPanel()
}

export function updateThemeSwitcher(currentTheme: 'light' | 'dark') {
  renderHeaderControls(currentTheme)
}

export function handleThemeToggle() {
  const currentTheme = getTheme()
  const nextTheme = currentTheme === 'light' ? 'dark' : 'light'
  setTheme(nextTheme)
  renderHeaderControls(nextTheme)
}
