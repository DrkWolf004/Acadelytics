export function showConfirmationPopup(message: string, title = 'Confirmación'): Promise<boolean> {
  return new Promise((resolve) => {
    const overlay = document.createElement('div')
    overlay.className = 'confirm-overlay'
    overlay.innerHTML = `
      <div class="confirm-dialog" role="dialog" aria-modal="true" aria-labelledby="confirm-title">
        <div class="confirm-header">
          <h2 id="confirm-title">${title}</h2>
          <button type="button" class="confirm-close" aria-label="Cerrar">&times;</button>
        </div>
        <div class="confirm-body">
          <p>${message}</p>
        </div>
        <div class="confirm-actions">
          <button type="button" class="button outline confirm-cancel">Cancelar</button>
          <button type="button" class="button danger confirm-confirm">Confirmar</button>
        </div>
      </div>
    `

    document.body.appendChild(overlay)

    const closeModal = (result: boolean) => {
      if (document.body.contains(overlay)) {
        document.body.removeChild(overlay)
      }
      resolve(result)
    }

    overlay.addEventListener('click', (event) => {
      if (event.target === overlay) {
        closeModal(false)
      }
    })

    overlay.querySelector<HTMLDivElement>('.confirm-dialog')?.addEventListener('click', (event) => {
      event.stopPropagation()
    })

    overlay.querySelector<HTMLButtonElement>('.confirm-close')?.addEventListener('click', () => closeModal(false))
    overlay.querySelector<HTMLButtonElement>('.confirm-cancel')?.addEventListener('click', () => closeModal(false))
    overlay.querySelector<HTMLButtonElement>('.confirm-confirm')?.addEventListener('click', () => closeModal(true))
  })
}
