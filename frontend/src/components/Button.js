import { MDCRipple } from '@material/ripple'

const makeRipples = qs => {
  for (let el of document.querySelectorAll(qs)) {
    new MDCRipple(el)
  }
}

makeRipples('.mdc-button')
// makeRipples('.mdc-icon-button')
