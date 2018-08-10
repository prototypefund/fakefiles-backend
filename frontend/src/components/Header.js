import { MDCRipple } from '@material/ripple'
import { MDCTopAppBar } from '@material/top-app-bar/index'

const iconButtonRipple = new MDCRipple(
  document.querySelector('.mdc-top-app-bar__action-item')
)
iconButtonRipple.unbounded = true

const topAppBarElement = document.querySelector('.mdc-top-app-bar')
topAppBarElement && new MDCTopAppBar(topAppBarElement)
