import { uploadFile, getFilesByClassFolder } from './services/fileService'
import type { FileRecord } from './types'

const ALLOWED_EXTENSIONS = ['.docx', '.xlsx', '.pptx', '.pdf', '.jpg', '.jpeg', '.png', '.zip', '.rar']

export async function createFileUploadUI(
  classFolderId: number,
  onFilesUpdated: (files: FileRecord[]) => void
): Promise<HTMLDivElement> {
  const container = document.createElement('div')
  container.className = 'files-upload-section'

  const inputId = `file-input-${classFolderId}`
  const progressContainerId = `progress-${classFolderId}`

  container.innerHTML = `
    <div style="margin-bottom: 16px;">
      <input 
        type="file" 
        id="${inputId}" 
        accept="${ALLOWED_EXTENSIONS.join(',')}"
        style="display: none;"
      />
      <label for="${inputId}" class="button primary file-upload-label">
        📁 Seleccionar archivo
      </label>
      <span style="margin-left: 12px; font-size: 0.9rem; color: var(--muted);">
        Extensiones permitidas: PDF, DOCX, XLSX, PPTX, JPG, PNG, ZIP, RAR
      </span>
    </div>
    <div id="${progressContainerId}"></div>
  `

  const fileInput = container.querySelector<HTMLInputElement>(`#${inputId}`)
  const progressContainer = container.querySelector<HTMLDivElement>(`#${progressContainerId}`)

  if (fileInput && progressContainer) {
    fileInput.addEventListener('change', async (event) => {
      const file = (event.target as HTMLInputElement).files?.[0]
      if (!file) return

      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
      if (!ALLOWED_EXTENSIONS.includes(fileExtension)) {
        showUploadError(progressContainer, `Extensión no permitida. Solo se aceptan: ${ALLOWED_EXTENSIONS.join(', ')}`)
        fileInput.value = ''
        return
      }

      const progressId = `file-progress-${Date.now()}`
      progressContainer.innerHTML = `
        <div id="${progressId}" style="
          margin-top: 12px;
          padding: 12px;
          background: var(--surface-strong);
          border-radius: 8px;
          border: 1px solid var(--border);
        ">
          <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            font-size: 0.9rem;
          ">
            <span style="color: var(--text-h); font-weight: 500;">${file.name}</span>
            <span id="${progressId}-percent" style="color: var(--muted);">0%</span>
          </div>
          <div style="
            width: 100%;
            height: 6px;
            background: var(--border);
            border-radius: 3px;
            overflow: hidden;
          ">
            <div id="${progressId}-bar" style="
              height: 100%;
              background: linear-gradient(90deg, var(--accent), #60a5fa);
              width: 0%;
              transition: width 0.3s ease;
              border-radius: 3px;
            "></div>
          </div>
        </div>
      `

      const progressBar = progressContainer.querySelector<HTMLDivElement>(`#${progressId}-bar`)
      const percentText = progressContainer.querySelector<HTMLSpanElement>(`#${progressId}-percent`)
      const progressElement = progressContainer.querySelector<HTMLDivElement>(`#${progressId}`)

      const result = await uploadFile(classFolderId, file, (progress) => {
        if (progressBar && percentText) {
          progressBar.style.width = `${progress}%`
          percentText.textContent = `${progress}%`
        }
      })

      fileInput.value = ''

      if (result.ok) {
        if (progressElement) {
          progressElement.innerHTML = `
            <div style="
              display: flex;
              align-items: center;
              gap: 8px;
              padding: 12px;
              background: rgba(34, 197, 94, 0.1);
              border: 1px solid rgba(34, 197, 94, 0.3);
              border-radius: 8px;
              color: #22c55e;
              font-weight: 500;
            ">
              <span>✓</span>
              <span>Archivo "${file.name}" subido exitosamente</span>
            </div>
          `
          setTimeout(() => {
            if (progressContainer.contains(progressElement)) {
              progressContainer.removeChild(progressElement)
            }
          }, 3000)
        }

        const filesResult = await getFilesByClassFolder(classFolderId)
        if (filesResult.ok && filesResult.data) {
          onFilesUpdated(filesResult.data)
        }
      } else {
        showUploadError(progressContainer, result.error || 'Error desconocido al subir archivo', progressElement)
      }
    })
  }

  return container
}

function showUploadError(
  progressContainer: HTMLDivElement,
  message: string,
  elementToRemove?: HTMLDivElement | null
) {
  if (elementToRemove && progressContainer.contains(elementToRemove)) {
    progressContainer.removeChild(elementToRemove)
  }

  const errorId = `file-error-${Date.now()}`
  const errorDiv = document.createElement('div')
  errorDiv.id = errorId
  errorDiv.style.cssText = `
    margin-top: 12px;
    padding: 12px;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    color: #ef4444;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
  `
  errorDiv.innerHTML = `
    <span>✕</span>
    <span>${message}</span>
  `

  progressContainer.appendChild(errorDiv)

  setTimeout(() => {
    if (progressContainer.contains(errorDiv)) {
      progressContainer.removeChild(errorDiv)
    }
  }, 5000)
}
