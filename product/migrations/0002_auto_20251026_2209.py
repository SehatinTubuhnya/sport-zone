from django.db import migrations
import os
import json

CATEGORY_CHOICES = [
    ('equipment', 'Equipment'),
    ('apparel', 'Apparel'),
    ('ball', 'Ball'),
]
VALID_CATEGORIES = [choice[0] for choice in CATEGORY_CHOICES]

def clean_price(price_str):
    if not isinstance(price_str, str):
        return 0
    
    cleaned_str = price_str.replace('Rp', '').replace('.', '').strip()
    try:
        return int(cleaned_str)
    except ValueError:
        return 0

def determine_category(name):
    name_lower = name.lower()
    if 'ball' in name_lower:
        return 'ball'
    if 't-shirt' in name_lower or 'short' in name_lower or 'jersey' in name_lower or 'apparel' in name_lower:
        return 'apparel'

    return 'equipment'

def load_data_from_json(apps, schema_editor):
    Product = apps.get_model('product', 'Product')

    MIGRATION_DIR = os.path.dirname(os.path.abspath(__file__))
    JSON_FILE_PATH = os.path.join(MIGRATION_DIR, '../fixtures/products.json')

    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"\n[Warning] File JSON 'products.json' tidak ditemukan. Melewatkan migrasi data.")
        return
    except json.JSONDecodeError:
        print(f"\n[Error] Gagal mem-parse 'products.json'. Pastikan format JSON valid.")
        return

    products_to_create = []
    for item in data:
        name = item.get('name')
        if not name: continue

        price_int = clean_price(item.get('price', '0'))

        images = item.get('images', [])
        thumbnail_url = images[0] if images else None

        category = determine_category(name)
        if category not in VALID_CATEGORIES:
            category = 'equipment'

        description = item.get('description', '')

        products_to_create.append(
            Product(
                name=name,
                price=price_int,
                description=description,
                category=category,
                thumbnail=thumbnail_url,
                is_featured=True,
                user=None
            )
        )

    if products_to_create:
        Product.objects.bulk_create(products_to_create, ignore_conflicts=True)

def remove_data(apps, schema_editor):
    Product = apps.get_model('product', 'Product')

    MIGRATION_DIR = os.path.dirname(os.path.abspath(__file__))
    JSON_FILE_PATH = os.path.join(MIGRATION_DIR, 'initial_products.json')

    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        product_names = [item.get('name') for item in data if item.get('name')]
        Product.objects.filter(name__in=product_names).delete()
    except (FileNotFoundError, json.JSONDecodeError):
        pass

class Migration(migrations.Migration):
    dependencies = [
        ('product', '0001_initial')
    ]

    operations = [
        migrations.RunPython(load_data_from_json, remove_data),
    ]
