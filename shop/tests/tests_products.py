from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from unittest.mock import patch
from shop.models import Product, Category

def create_test_image():
    return SimpleUploadedFile(name='test_image.jpg', content=b'\x47\x49\x46\x38\x89\x61', content_type='image/jpeg')

class TestModelProduct(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Books", slug="name")
        self.product = Product.objects.create(title="Book1", price=100, category=self.category, image=create_test_image())

    def test_product_count(self):
        self.assertEqual(Product.objects.count(), 1)

    def test_product_string_returns_title(self):
        self.assertEqual(str(self.product), "Book1")

    def test_product_price_should_be_positive(self):
        negative_price = Product.objects.create(title="Book2", price=-100, category=self.category, image=create_test_image())
        with self.assertRaises(ValidationError):
            negative_price.full_clean()

    def test_optional_fields_can_be_blank(self):
        self.product.full_clean()
        self.assertIsNone(self.product.description)
        self.assertIsNone(self.product.short_description)

    def test_product_and_category_relationship(self):
        self.assertEqual(self.product.category.name, "Books")
        self.assertIn(self.product, self.category.products.all())

    def test_created_at_is_set_automatically(self):
        self.assertIsNotNone(self.product.created_at)


class TestViewsProductDetail(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Books", slug="name")
        self.product = Product.objects.create(title="Book1", price=100, category=self.category, image=create_test_image())

    def test_product_detail_view_renders_correctly(self):
        url = reverse('product_detail', args=[self.product.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')

        self.assertEqual(response.context['product'], self.product)
        self.assertIn('related_products', response.context)
        self.assertIn('year', response.context)

    def test_product_detail_view_returns_404_if_missing(self):
        url = reverse('product_detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_products_filtering(self):
        other = Product.objects.create(title="Book1", price=50, category=self.category, image=create_test_image())
        unrelated = Product.objects.create(title="Random Item", price=10, image=create_test_image(),
                                           category=Category.objects.create(name="Random"))

        url = reverse('product_detail', args=[self.product.pk])
        response = self.client.get(url)
        related_products = response.context['related_products']

        self.assertIn(other, related_products)
        self.assertNotIn(unrelated, related_products)


class TestViewsProducts(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Books")
        self.other_category = Category.objects.create(name="Random", slug="name")
        self.product1 = Product.objects.create(title="Monitor", price=20, category=self.category, image=create_test_image())
        self.product2 = Product.objects.create(title="Keyboard", price=20, category=self.category, image=create_test_image())
        self.unrelated_product = Product.objects.create(title="Novel", price=20, category=self.other_category, image=create_test_image())

    def test_products_by_category_renders_correctly(self):
        url = reverse('products_by_category', args=[self.category.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products.html')
        self.assertEqual(response.context['category'], self.category)

        products = list(response.context['products'])
        self.assertIn(self.product1, products)
        self.assertIn(self.product2, products)
        self.assertNotIn(self.unrelated_product, products)

    def test_products_by_category_invalid_id(self):
        url = reverse('products_by_category', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @patch('shop.views.get_object_or_404')
    def test_products_by_category_uses_get_object_or_404(self, mock_get):
        mock_get.return_value = self.category
        url = reverse('products_by_category', args=[self.category.id])
        self.client.get(url)
        mock_get.assert_called_once_with(Category, id=self.category.id)


