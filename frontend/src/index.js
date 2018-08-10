'use strict'

if (module.hot) {
  module.hot.accept()
}

import 'babel-polyfill'

// components
import './components/Button.js'
import './components/Header.js'
import './components/Nav.js'
import './components/ShareDialog.js'

// views
import './views/index.js'

// style
import './index.scss'
