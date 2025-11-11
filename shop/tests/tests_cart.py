import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from shop.models import Cart, CartItem, Product, Category, Customer

def create_test_image():
    return SimpleUploadedFile(name='test_image.jpg', content=b'\x47\x49\x46\x38\x89\x61', content_type='image/jpeg')

class TestModelCart(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Books", slug="books")
        self.product1 = Product.objects.create(title="Book A", price=50, category=self.category, image=create_test_image())
        self.product2 = Product.objects.create(title="Book B", price=30, category=self.category, image=create_test_image())

        self.user = User.objects.create_user(username="johndoe", password="password123")
        self.customer = Customer.objects.create(name="John Doe", email="john@example.com", user=self.user)
        self.cart = Cart.objects.create(customer=self.customer)
        self.item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)

    def test_cart_creation(self):
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(self.cart.customer, self.customer)
        self.assertIsNotNone(self.cart.created_at)

    def test_cartitem_creation(self):
        self.assertEqual(self.item.cart, self.cart)
        self.assertEqual(self.item.product, self.product1)
        self.assertEqual(self.item.quantity, 2)

    def test_total_price(self):
        expected = self.product1.price * 2
        self.assertEqual(self.item.total_price, expected)

    def test_multiple_items_in_cart(self):
        item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

        items = list(self.cart.items.all())
        self.assertIn(item1, items)
        self.assertIn(item2, items)

    def test_deleting_cart_should_delete_cartitem(self):
        self.assertEqual(CartItem.objects.count(), 1)

        self.cart.delete()
        self.assertEqual(CartItem.objects.count(), 0)

    def test_deleting_product_should_delete_cartitem(self):
        self.product1.delete()
        self.assertEqual(CartItem.objects.count(), 0)

    def test_deleting_customer_should_delete_cart(self):
        self.customer.delete()
        self.assertEqual(Cart.objects.count(), 0)
        self.assertEqual(CartItem.objects.count(), 0)


class TestViewsCart(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(title="Book1", price=100, category=self.category, image=create_test_image())

        self.user = User.objects.create_user(username="john", password="password123")
        self.customer = Customer.objects.create(user=self.user, name="John Doe", email="john@example.com")

    def test_add_item_authenticated_user(self):
        self.client.login(username="john", password="password123")
        payload = {"productId": self.product.id, "action": "add", "quantity": 2}
        response = self.client.post(reverse("update_cart"), data=json.dumps(payload), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "Cart updated successfully (auth user)"})

        cart = Cart.objects.get(customer=self.customer)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_remove_item_authenticated_user(self):
        self.client.login(username="john", password="password123")
        cart = Cart.objects.create(customer=self.customer)
        CartItem.objects.create(cart=cart, product=self.product, quantity=3)

        payload = {"productId": self.product.id, "action": "remove"}
        self.client.post(reverse("update_cart"), data=json.dumps(payload), content_type="application/json")

        self.assertFalse(CartItem.objects.filter(cart=cart, product=self.product).exists())

    def test_add_item_guest_user(self):
        payload = {"productId": self.product.id, "action": "add", "quantity": 1}
        response = self.client.post(reverse("update_cart"), data=json.dumps(payload), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("cart", response.cookies)
        cart_cookie = json.loads(response.cookies["cart"].value)
        self.assertEqual(cart_cookie[str(self.product.id)]["quantity"], 1)

    def test_delete_item_guest_user(self):
        cart_data = {str(self.product.id): {"quantity": 1}}
        self.client.cookies["cart"] = json.dumps(cart_data)
        payload = {"productId": self.product.id, "action": "delete"}
        response = self.client.post(reverse("update_cart"), data=json.dumps(payload), content_type="application/json")

        cart_cookie = json.loads(response.cookies["cart"].value)
        self.assertNotIn(str(self.product.id), cart_cookie)

    def test_cart_view_authenticated_user(self):
        self.client.login(username="john", password="password123")
        cart = Cart.objects.create(customer=self.customer)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        response = self.client.get(reverse("cart_view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cart.html")

        self.assertIn("cart", response.context)
        self.assertIn("cart_items", response.context)
        self.assertIn("total", response.context)
        self.assertEqual(float(response.context["total"]), 200)

    def test_view_empty_cart_guest(self):
        response = self.client.get(reverse("cart_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 0)
        self.assertEqual(response.context["cart_items"], [])