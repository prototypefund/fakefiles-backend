import { MDCDialog } from '@material/dialog'

const dialog = new MDCDialog(document.querySelector('#share-dialog'))
const dialogToggle = document.querySelector('[data-share]')
dialogToggle.addEventListener('click', evt => {
  dialog.lastFocusedTarget = evt.target
  dialog.show()
})
