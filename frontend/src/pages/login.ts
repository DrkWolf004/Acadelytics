import { login } from '../services/authService'
import { setAuthStorage } from '../hooks/useLocalStorage'

export function renderLoginPage(root: HTMLElement) {
  root.innerHTML = `
    <main class="page page-auth">
      <section class="auth-card">
        <div class="auth-header">
          <h1>Iniciar sesión</h1>
          <div id="header-controls" class="header-controls"></div>
        </div>
        <p>Accede a tu cuenta para comenzar a revisar el estado académico y tus reportes.</p>
        <form id="login-form" class="auth-form">
          <label>
            Correo electrónico
            <input type="email" name="correo" placeholder="tucorreo@ejemplo.com" required />
          </label>
          <label>
            Contraseña
            <input type="password" name="password" placeholder="********" required minlength="6" />
          </label>
          <button type="submit" class="button primary">Entrar</button>
        </form>
        <p class="auth-footer">¿No tienes cuenta? <a href="#/register" data-router>Registrarse</a></p>
        <div id="login-error" class="form-error"></div>
      </section>
    </main>
  `

  const form = document.querySelector<HTMLFormElement>('#login-form')
  const errorMessage = document.querySelector<HTMLDivElement>('#login-error')

  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    errorMessage!.textContent = ''

    const formData = new FormData(form)
    const correo = formData.get('correo')?.toString().trim() ?? ''
    const password = formData.get('password')?.toString().trim() ?? ''

    try {
      const result = await login({ correo, password })
      if (result.ok && result.data) {
        setAuthStorage(result.data.token, result.data)
        window.location.hash = '#/dashboard'
      } else {
        errorMessage!.textContent = result.error || 'No se pudo iniciar sesión.'
      }
    } catch (error) {
      errorMessage!.textContent = 'Error de conexión con el servidor.'
    }
  })
}
