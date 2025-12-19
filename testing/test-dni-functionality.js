(function() {
  var phoneNodes = document.querySelectorAll('.callrail-phone-number');
  if (!phoneNodes.length) {
    console.warn('No DNI phone numbers found.');
    return;
  }

  phoneNodes.forEach(function(node) {
    console.log('DNI phone number detected:', node.textContent.trim());
  });
})();
