console.log("cart.js loaded ✅");
document.addEventListener("DOMContentLoaded", function () {
  const addBtn = document.getElementById("add-to-cart-btn");
  if (addBtn) {
    addBtn.addEventListener("click", function () {
      const productId = this.dataset.product;
      const quantityInput = document.getElementById("quantity");
      const quantity = quantityInput ? parseInt(quantityInput.value) || 1 : 1;
      updateCart(productId, "add", quantity);
    });
  }

  const cartButtons = document.querySelectorAll(".cart-action");
  cartButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      const productId = this.dataset.product;
      const action = this.dataset.action;
      updateCart(productId, action, 1);
    });
  });
});

function updateCart(productId, action, quantity = 1) {
  fetch("/update-cart/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      productId: productId,
      action: action,
      quantity: quantity,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("Cart response:", data);

      showAlert(data.message || "Cart updated");

      if (window.location.pathname === "/cart/") {
        setTimeout(() => location.reload(), 500);
      }
    })
    .catch((err) => console.error("Error updating cart:", err));
}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function showAlert(message) {
  const alert = document.createElement("div");
  alert.textContent = message;
  alert.className =
    "alert alert-success position-fixed top-0 start-50 translate-middle-x mt-3 px-4 py-2 shadow fw-semibold";
  alert.style.zIndex = "1055";
  document.body.appendChild(alert);

  setTimeout(() => alert.remove(), 2000);
}
