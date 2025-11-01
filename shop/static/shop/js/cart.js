document.addEventListener('DOMContentLoaded', () => {
  const addBtn = document.getElementById('add-to-cart-btn');
  if (!addBtn) return;

  addBtn.addEventListener('click', () => {
    const productId = addBtn.dataset.product;
    const quantity = parseInt(document.getElementById('quantity').value);

    fetch('/update-cart/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        productId: productId,
        action: 'add',
        quantity: quantity,
      }),
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
    })
    .catch(err => console.error('Error:', err));
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
