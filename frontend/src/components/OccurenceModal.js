import { MDCDialog } from '@material/dialog'

for (let toggle of document.querySelectorAll('[data-occurence-open]')) {
  const id = toggle.dataset.occurenceId
  const dialog = new MDCDialog(document.querySelector(`#occurence-modal-${id}`))
  toggle.addEventListener('click', evt => {
    evt.preventDefault()
    dialog.lastFocusedTarget = evt.target
    dialog.show()
  })
}
