import { register } from '../services/authService'
import { setAuthStorage } from '../hooks/useLocalStorage'

export function renderRegisterPage(root: HTMLElement) {
  root.innerHTML = `
    <main class="page page-auth">
      <section class="auth-card">
        <div class="auth-header">
          <h1>Crear cuenta</h1>
          <div id="header-controls" class="header-controls"></div>
        </div>
        <p>Regístrate con tus datos para empezar a usar Acadelytics y gestionar tus resultados.</p>
        <form id="register-form" class="auth-form">
          <label>
            Nombre
            <input type="text" name="nombre" placeholder="Tu nombre" required />
          </label>
          <label>
            Apellido
            <input type="text" name="apellido" placeholder="Tu apellido" required />
          </label>
          <label>
            Correo electrónico
            <input type="email" name="correo" placeholder="tucorreo@ejemplo.com" required />
          </label>
          <label>
            Rol
            <select name="rol" required>
              <option value="Alumno">Alumno</option>
              <option value="Profesor">Profesor</option>
            </select>
          </label>
          <label>
            Contraseña
            <input type="password" name="password" placeholder="********" required minlength="8" />
          </label>
          <button type="submit" class="button primary">Registrarse</button>
        </form>
        <p class="auth-footer">¿Ya tienes cuenta? <a href="#/login" data-router>Logearse</a></p>
        <div id="register-error" class="form-error"></div>
      </section>
    </main>
  `

  const form = document.querySelector<HTMLFormElement>('#register-form')
  const errorMessage = document.querySelector<HTMLDivElement>('#register-error')

  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    errorMessage!.textContent = ''

    const formData = new FormData(form)
    const payload = {
      nombre: formData.get('nombre')?.toString().trim() ?? '',
      apellido: formData.get('apellido')?.toString().trim() ?? '',
      correo: formData.get('correo')?.toString().trim() ?? '',
      password: formData.get('password')?.toString().trim() ?? '',
      rol: formData.get('rol')?.toString().trim() || 'Alumno',
    }

    try {
      const result = await register(payload)
      if (result.ok && result.data) {
        setAuthStorage(result.data.token, result.data)
        window.location.hash = '#/dashboard'
      } else {
        errorMessage!.textContent = result.error || 'No se pudo crear la cuenta.'
      }
    } catch (error) {
      errorMessage!.textContent = 'Error de conexión con el servidor.'
    }
  })
}
