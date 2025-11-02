document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.cart-action');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const productId = btn.dataset.product;
      const action = btn.dataset.action;

      fetch('/update-cart/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
          productId: productId,
          action: action,
          quantity: 1
        }),
      })
      .then(res => res.json())
      .then(() => location.reload());
    });
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
