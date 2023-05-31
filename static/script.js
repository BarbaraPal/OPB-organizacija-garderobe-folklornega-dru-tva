function checkCustomOption(value) {
  var customOptionInput = document.getElementById('customOptionInput');
  if (value === 'custom') {
    customOptionInput.style.display = 'block';
  } else {
    customOptionInput.style.display = 'none';
  }
}
