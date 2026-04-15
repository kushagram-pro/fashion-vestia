from app.services.outfit_generator import generate_outfit

wardrobe = [
    {"label": "Black T-Shirt", "category": "top", "color": "black"},
    {"label": "Blue Jeans", "category": "bottom", "color": "blue"},
    {"label": "White Sneakers", "category": "shoes", "color": "white"}
]

user = {
    "body_type": "athletic",
    "skin_tone": "medium",
    "style": "casual",
    "gender": "any"
}

result = generate_outfit(
    wardrobe,
    user,
    occasion="Everyday Casual",
    weather="32°C, sunny"
)

print(result)