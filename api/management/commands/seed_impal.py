from django.core.management.base import BaseCommand
from django.utils.text import slugify

from api.models import Category, Product, SiteSettings


PRODUCTS = [
    {
        "name": "Impal Premium Crystal Sugar",
        "category": "Sugar",
        "weight": "1kg",
        "weights": ["500g", "1kg", "5kg"],
        "description": "Sparkling, high-grade sugar crystals that dissolve perfectly without impurities.",
        "price": 64,
        "old_price": 75,
        "stock": 250,
        "rating": 4.8,
        "reviews": 142,
        "image": "https://images.unsplash.com/photo-1581781868515-51543be28646?auto=format&fit=crop&q=80&w=600",
        "is_featured": True,
        "tag": "Best Seller",
    },
    {
        "name": "Impal Superfine Raw Brown Sugar",
        "category": "Sugar",
        "weight": "1kg",
        "weights": ["1kg", "2kg"],
        "description": "Rich molasses flavour with no artificial additives, perfect for baking and daily brewing.",
        "price": 95,
        "old_price": 110,
        "stock": 120,
        "rating": 4.9,
        "reviews": 88,
        "image": "https://images.unsplash.com/photo-1608686207856-001b95cf60ca?auto=format&fit=crop&q=80&w=600",
        "is_featured": True,
        "tag": "Organic",
    },
    {
        "name": "Impal Premium Thin Poha",
        "category": "Poha",
        "weight": "500g",
        "weights": ["500g", "1kg"],
        "description": "Light, authentic texture from selected high-quality paddy grains.",
        "price": 48,
        "old_price": 55,
        "stock": 180,
        "rating": 4.7,
        "reviews": 205,
        "image": "https://images.unsplash.com/photo-1596797038530-2c107229654b?auto=format&fit=crop&q=80&w=600",
        "is_featured": True,
        "tag": "Super Light",
    },
    {
        "name": "Impal Premium Medium Poha",
        "category": "Poha",
        "weight": "1kg",
        "weights": ["500g", "1kg", "2kg"],
        "description": "Balanced poha for wholesome family breakfasts and traditional recipes.",
        "price": 55,
        "old_price": 65,
        "stock": 300,
        "rating": 4.9,
        "reviews": 312,
        "image": "https://images.unsplash.com/photo-1613292443284-8d10ef9383fe?auto=format&fit=crop&q=80&w=600",
        "is_featured": True,
        "tag": "Chef's Choice",
    },
    {
        "name": "Impal High-Fiber Thick Poha",
        "category": "Poha",
        "weight": "1kg",
        "weights": ["1kg", "5kg"],
        "description": "Thick, nutrient-dense flattened rice for chivda, frying, and steamed snacks.",
        "price": 58,
        "old_price": 70,
        "stock": 150,
        "rating": 4.6,
        "reviews": 95,
        "image": "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&q=80&w=600",
        "is_featured": False,
        "tag": "High Fiber",
    },
]


class Command(BaseCommand):
    help = "Seed IMPAL Food categories, products, and site settings"

    def handle(self, *args, **options):
        categories = {}
        for name in ["Sugar", "Poha"]:
            category, _ = Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            categories[name] = category

        for item in PRODUCTS:
            category = categories[item.pop("category")]
            Product.objects.update_or_create(
                name=item["name"],
                defaults={**item, "category": category, "is_visible": True},
            )

        SiteSettings.objects.update_or_create(
            id=1,
            defaults={
                "brand_name": "Impal Food",
                "tagline": "Purity. Trust. Quality.",
                "hero_description": "At IMPAL, we bring you the finest daily essentials directly from the heart of India's richest agricultural hubs. Packed with utmost care, hygiene, and transparency, we ensure that every grain adds sweetness, health, and joy to your family's daily meals.",
                "about_heading": "Specializing in the Two Pillars of Every Indian Pantry",
                "about_p1": "At IMPAL, our journey started with a simple belief: the most essential ingredients in your kitchen deserve the highest standard of care. We chose to specialize in the two pillars of every household pantry — Premium Sugar and Authentic Poha.",
                "about_p2": "We understand what makes a perfect batch. For our Poha, we select high-quality paddy grains to give you that authentic texture and lightness that central India loves. For our Sugar, we ensure sparkling, high-grade crystals that dissolve perfectly without any impurities.",
                "about_p3": "What sets IMPAL apart is our strict focus on modern, untouched-by-hand packaging and rigorous quality checks. We bridge the gap between the finest fields and your modern kitchen, ensuring that every sealed pouch of IMPAL Sugar and Poha brings health, hygiene, and happiness to your family.",
                "hero_image": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&q=80&w=1200",
                "whatsapp_number": "+919993408621",
                "address": "44/4, Pardeshipura, Indore (M.P) - 452003",
                "email": "impalfoodscontact@gmail.com",
                "phone": "+91 99934 08621",
                "meta_title": "IMPAL Food | Purity. Trust. Quality.",
                "meta_desc": "Premium Sugar and Authentic Poha from India's agricultural hubs.",
                "meta_keywords": "IMPAL food, sugar, poha, Indore, premium sugar, authentic poha",
            },
        )

        self.stdout.write(self.style.SUCCESS("IMPAL backend seed completed."))
