import { register } from '../services/authService'
import { setAuthStorage } from '../hooks/useLocalStorage'
import { submitProfessorValidation } from '../services/professorValidationService'

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
            <select id="register-role" name="rol" required>
              <option value="Alumno">Alumno</option>
              <option value="Profesor">Profesor</option>
            </select>
          </label>
          <label id="validation-file-label" style="display:none;">
            Documento de validación para profesor
            <input type="file" name="validationFile" accept=".pdf,.doc,.docx,.jpg,.jpeg,.png" />
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
  const roleSelect = document.querySelector<HTMLSelectElement>('#register-role')
  const validationFileLabel = document.querySelector<HTMLLabelElement>('#validation-file-label')

  const updateFileFieldVisibility = () => {
    if (!roleSelect || !validationFileLabel) return
    validationFileLabel.style.display = roleSelect.value === 'Profesor' ? 'block' : 'none'
  }

  roleSelect?.addEventListener('change', updateFileFieldVisibility)
  updateFileFieldVisibility()

  form?.addEventListener('submit', async (event) => {
    event.preventDefault()
    errorMessage!.textContent = ''

    const formData = new FormData(form)
    const selectedRole = formData.get('rol')?.toString().trim() || 'Alumno'
    const validationFile = formData.get('validationFile') as File | null

    if (selectedRole === 'Profesor') {
      if (!validationFile || !validationFile.name) {
        errorMessage!.textContent = 'Debes adjuntar un documento para solicitar el rol de Profesor.'
        return
      }
    }

    const payload = {
      nombre: formData.get('nombre')?.toString().trim() ?? '',
      apellido: formData.get('apellido')?.toString().trim() ?? '',
      correo: formData.get('correo')?.toString().trim() ?? '',
      password: formData.get('password')?.toString().trim() ?? '',
      rol: 'Alumno',
    }

    try {
      const result = await register(payload)
      if (result.ok && result.data) {
        setAuthStorage(result.data.token, result.data)

        if (selectedRole === 'Profesor' && validationFile && validationFile.name) {
          const validationResult = await submitProfessorValidation(validationFile)
          if (!validationResult.ok) {
            errorMessage!.textContent = validationResult.error || 'No se pudo enviar la solicitud de validación.'
            return
          }
        }

        window.location.hash = '#/dashboard'
      } else {
        errorMessage!.textContent = result.error || 'No se pudo crear la cuenta.'
      }
    } catch (error) {
      errorMessage!.textContent = 'Error de conexión con el servidor.'
    }
  })
}
