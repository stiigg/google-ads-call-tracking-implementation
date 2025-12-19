(function() {
  function getGclid() {
    var params = new URLSearchParams(window.location.search);
    return params.get('gclid');
  }

  var gclid = getGclid();
  if (gclid) {
    console.log('GCLID detected:', gclid);
  } else {
    console.warn('No GCLID found in URL');
  }
})();
