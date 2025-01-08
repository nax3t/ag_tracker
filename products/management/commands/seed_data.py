from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Seed the database with sample users and products'

    def handle(self, *args, **options):
        # Create test users if they don't exist
        users = []
        for i in range(1, 4):
            username = f'test_user_{i}'
            email = f'test{i}@example.com'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_active': True
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            users.append(user)

        # Sample product data
        products_data = [
            {
                'name': 'Corn Seeds',
                'category': 'SEED',
                'quantity': Decimal('500'),
                'unit': 'G',
                'cost_per_unit': Decimal('0.05'),
                'minimum_stock': Decimal('100'),
                'description': 'High-yield corn seeds',
                'supplier': 'FarmSeeds Co.',
                'location': 'Seed Storage A1'
            },
            {
                'name': 'NPK Fertilizer',
                'category': 'FERT',
                'quantity': Decimal('50'),
                'unit': 'KG',
                'cost_per_unit': Decimal('2.50'),
                'minimum_stock': Decimal('10'),
                'description': 'Balanced NPK 15-15-15',
                'supplier': 'GrowMore Ltd',
                'location': 'Chemical Store B2'
            },
            {
                'name': 'Organic Pesticide',
                'category': 'PEST',
                'quantity': Decimal('5'),
                'unit': 'L',
                'cost_per_unit': Decimal('15.00'),
                'minimum_stock': Decimal('1'),
                'description': 'Natural pest control solution',
                'supplier': 'EcoFarm Solutions',
                'location': 'Chemical Store B3'
            },
            {
                'name': 'Garden Hoe',
                'category': 'TOOL',
                'quantity': Decimal('10'),
                'unit': 'UNIT',
                'cost_per_unit': Decimal('25.00'),
                'minimum_stock': Decimal('2'),
                'description': 'Durable steel garden hoe',
                'supplier': 'FarmTools Inc',
                'location': 'Tool Shed C1'
            },
            {
                'name': 'Chicken Feed',
                'category': 'FEED',
                'quantity': Decimal('200'),
                'unit': 'KG',
                'cost_per_unit': Decimal('1.75'),
                'minimum_stock': Decimal('50'),
                'description': 'Premium chicken feed mix',
                'supplier': 'FeedMaster Co',
                'location': 'Feed Storage D1'
            }
        ]

        # Create products for each user
        for user in users:
            for product_data in products_data:
                # Add some variation to quantities and costs
                quantity_variation = Decimal(str(random.uniform(0.8, 1.2)))
                cost_variation = Decimal(str(random.uniform(0.9, 1.1)))
                
                product_data_copy = product_data.copy()
                product_data_copy['quantity'] *= quantity_variation
                product_data_copy['cost_per_unit'] *= cost_variation
                
                # Add random expiry dates for some products
                if random.choice([True, False]):
                    days_to_expiry = random.randint(30, 365)
                    product_data_copy['expiry_date'] = timezone.now().date() + timezone.timedelta(days=days_to_expiry)

                product, created = Product.objects.get_or_create(
                    name=product_data_copy['name'],
                    user=user,
                    defaults=product_data_copy
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created product: {product.name} for user: {user.username}'
                        )
                    )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database')) 