import { MDCTextField } from '@material/textfield'

for (let field of document.querySelectorAll('.mdc-text-field'))
  new MDCTextField(field)

// import {MDCTextFieldHelperText} from '@material/textfield/helper-text';

// const helperText = new MDCTextFieldHelperText(document.querySelector('.mdc-text-field-helper-text'));
