import { MDCTemporaryDrawer } from '@material/drawer'

const drawer = new MDCTemporaryDrawer(
  document.querySelector('.mdc-drawer--temporary')
)

const navToggle = document.querySelector('[data-nav-toggle]')
navToggle && navToggle.addEventListener('click', () => (drawer.open = true))
