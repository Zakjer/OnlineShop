from django.test import TestCase, Client
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from shop.admin import CategoryAdmin, ProductAdmin, CustomerAdmin, CartAdmin, CartItemAdmin
from shop.models import Category, Product, Customer, Cart, CartItem

class TestAdmin(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='password123')
        self.client = Client()
        self.client.login(username='admin', password='password123')

        self.category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(title="Book A", price=50.00, category=self.category, stock=10)
        self.customer_user = User.objects.create_user(username='john', password='password')
        self.customer = Customer.objects.create(user=self.customer_user, name="John Doe", email="john@example.com")
        self.cart = Cart.objects.create(customer=self.customer)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.site = AdminSite()

    def test_category_admin_registered(self):
        admin_instance = CategoryAdmin(Category, self.site)
        self.assertEqual(admin_instance.list_display, ('id', 'name', 'slug'))
        self.assertEqual(admin_instance.search_fields, ('name',))
        self.assertEqual(admin_instance.prepopulated_fields, {'slug': ('name',)})
        self.assertEqual(admin_instance.ordering, ('name',))

    def test_product_admin_configuration(self):
        admin_instance = ProductAdmin(Product, self.site)
        self.assertEqual(admin_instance.list_display, ('id', 'title', 'category', 'price', 'discount_price', 'stock', 'created_at'))
        self.assertEqual(admin_instance.list_filter, ('category', 'created_at'))
        self.assertEqual(admin_instance.search_fields, ('title', 'category__name'))

    def test_customer_admin_configuration(self):
        admin_instance = CustomerAdmin(Customer, self.site)
        self.assertEqual(admin_instance.list_display, ('id', 'user', 'name', 'email'))
        self.assertEqual(admin_instance.search_fields, ('user__username', 'name', 'email'))

    def test_cart_admin_configuration(self):
        admin_instance = CartAdmin(Cart, self.site)
        self.assertEqual(admin_instance.list_display, ('id', 'customer', 'created_at'))
        self.assertEqual(admin_instance.search_fields, ('customer__user__username',))
        self.assertEqual(admin_instance.ordering, ('-created_at',))

    def test_cartitem_admin_configuration(self):
        admin_instance = CartItemAdmin(CartItem, self.site)
        self.assertEqual(admin_instance.list_display, ('id', 'cart', 'product', 'quantity', 'total_price'))
        self.assertEqual(admin_instance.list_filter, ('cart', 'product'))
        self.assertEqual(admin_instance.search_fields, ('product__title',))

    def test_admin_pages_access(self):
        urls = [
            '/admin/shop/category/',
            '/admin/shop/product/',
            '/admin/shop/customer/',
            '/admin/shop/cart/',
            '/admin/shop/cartitem/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)