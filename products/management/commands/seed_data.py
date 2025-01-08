from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone
from decimal import Decimal
import random
from typing import Dict, List

class Command(BaseCommand):
    help = 'Seed the database with sample users and products'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing products before seeding',
        )

    def get_farm_locations(self) -> List[Dict]:
        return [
            {
                'name': 'Central Valley Farm',
                'city': 'Fresno',
                'state': 'CA',
                'lat': 36.7378,
                'lng': -119.7871
            },
            {
                'name': 'Midwest Grain Storage',
                'city': 'Des Moines',
                'state': 'IA',
                'lat': 41.5868,
                'lng': -93.6250
            },
            {
                'name': 'Southern Livestock Farm',
                'city': 'Dallas',
                'state': 'TX',
                'lat': 32.7767,
                'lng': -96.7970
            },
            {
                'name': 'Northeast Dairy',
                'city': 'Burlington',
                'state': 'VT',
                'lat': 44.4759,
                'lng': -73.2121
            },
            {
                'name': 'Pacific Northwest Orchard',
                'city': 'Yakima',
                'state': 'WA',
                'lat': 46.6021,
                'lng': -120.5059
            },
            {
                'name': 'Florida Citrus Grove',
                'city': 'Orlando',
                'state': 'FL',
                'lat': 28.5383,
                'lng': -81.3792
            },
            {
                'name': 'Montana Wheat Fields',
                'city': 'Great Falls',
                'state': 'MT',
                'lat': 47.5002,
                'lng': -111.3008
            },
        ]

    def handle(self, *args, **options):
        if options['clear']:
            # Clear existing products
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all existing products'))
            
            # Optionally clear users (commented out for safety)
            # User.objects.exclude(is_superuser=True).delete()
            # self.stdout.write(self.style.SUCCESS('Cleared all non-superuser users'))

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

        # Base product templates
        product_templates = {
            'SEED': [
                {'name': 'Corn Seeds', 'unit': 'G', 'base_quantity': 500, 'cost_per_unit': 0.05},
                {'name': 'Tomato Seeds', 'unit': 'G', 'base_quantity': 250, 'cost_per_unit': 0.08},
                {'name': 'Wheat Seeds', 'unit': 'KG', 'base_quantity': 25, 'cost_per_unit': 2.50},
            ],
            'FERT': [
                {'name': 'NPK Fertilizer', 'unit': 'KG', 'base_quantity': 50, 'cost_per_unit': 2.50},
                {'name': 'Organic Compost', 'unit': 'KG', 'base_quantity': 100, 'cost_per_unit': 1.75},
            ],
            'PEST': [
                {'name': 'Organic Pesticide', 'unit': 'L', 'base_quantity': 5, 'cost_per_unit': 15.00},
                {'name': 'Insect Repellent', 'unit': 'L', 'base_quantity': 3, 'cost_per_unit': 12.50},
            ],
            'TOOL': [
                {'name': 'Garden Hoe', 'unit': 'UNIT', 'base_quantity': 10, 'cost_per_unit': 25.00},
                {'name': 'Pruning Shears', 'unit': 'UNIT', 'base_quantity': 15, 'cost_per_unit': 18.50},
            ],
            'FEED': [
                {'name': 'Chicken Feed', 'unit': 'KG', 'base_quantity': 200, 'cost_per_unit': 1.75},
                {'name': 'Cattle Feed', 'unit': 'KG', 'base_quantity': 500, 'cost_per_unit': 1.25},
            ],
            'LIVE': [
                {'name': 'Layer Chickens', 'unit': 'UNIT', 'base_quantity': 50, 'cost_per_unit': 15.00},
                {'name': 'Dairy Cows', 'unit': 'UNIT', 'base_quantity': 5, 'cost_per_unit': 1200.00},
            ],
            'CROP': [
                {'name': 'Sweet Corn', 'unit': 'KG', 'base_quantity': 1000, 'cost_per_unit': 2.00},
                {'name': 'Tomatoes', 'unit': 'KG', 'base_quantity': 500, 'cost_per_unit': 3.50},
            ],
        }

        farm_locations = self.get_farm_locations()
        
        # Create products for each user
        for user in users:
            for category, templates in product_templates.items():
                # Randomly select 1-3 products from each category
                selected_templates = random.sample(templates, random.randint(1, len(templates)))
                
                for template in selected_templates:
                    # Add variation to quantities and costs
                    quantity_variation = Decimal(str(random.uniform(0.5, 2.0)))
                    cost_variation = Decimal(str(random.uniform(0.9, 1.1)))
                    
                    # Select random farm location
                    location = random.choice(farm_locations)
                    
                    product_data = {
                        'name': template['name'],
                        'category': category,
                        'quantity': Decimal(str(template['base_quantity'])) * quantity_variation,
                        'unit': template['unit'],
                        'cost_per_unit': Decimal(str(template['cost_per_unit'])) * cost_variation,
                        'minimum_stock': Decimal(str(template['base_quantity'])) * Decimal('0.2'),  # 20% of base quantity
                        'description': f"Sample {template['name']} for testing",
                        'supplier': f"{template['name']} Supplier Co.",
                        'location': f"{location['name']}, {location['city']}, {location['state']}",
                        'latitude': Decimal(str(location['lat'])),
                        'longitude': Decimal(str(location['lng'])),
                    }
                    
                    # Add random expiry dates for some products
                    if random.choice([True, False]):
                        days_to_expiry = random.randint(30, 365)
                        product_data['expiry_date'] = timezone.now().date() + timezone.timedelta(days=days_to_expiry)

                    product, created = Product.objects.get_or_create(
                        name=product_data['name'],
                        user=user,
                        defaults=product_data
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Created product: {product.name} for user: {user.username}'
                            )
                        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database')) 