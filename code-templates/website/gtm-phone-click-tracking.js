(function() {
  function trackPhoneClick(event) {
    var target = event.target.closest('a[href^="tel:"]');
    if (!target) {
      return;
    }

    var phoneNumber = target.getAttribute('href');
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'phone_click',
      phone_number: phoneNumber,
      click_text: target.textContent.trim()
    });
  }

  document.addEventListener('click', trackPhoneClick);
})();
