import os

folders = [
    "vestia-ai/app/core",
    "vestia-ai/app/models",
    "vestia-ai/app/services",
    "vestia-ai/app/routes",
    "vestia-ai/app/data",
    "vestia-ai/app/utils",
    "vestia-ai/uploads"
]

files = [
    "vestia-ai/app/main.py",
    "vestia-ai/app/core/config.py",
    "vestia-ai/app/core/ollama_client.py",
    "vestia-ai/app/models/clothing.py",
    "vestia-ai/app/models/user.py",
    "vestia-ai/app/services/wardrobe_service.py",
    "vestia-ai/app/services/image_analyzer.py",
    "vestia-ai/app/services/outfit_generator.py",
    "vestia-ai/app/routes/wardrobe.py",
    "vestia-ai/app/routes/outfit.py",
    "vestia-ai/app/data/wardrobe.json",
    "vestia-ai/app/data/users.json",
    "vestia-ai/app/utils/helpers.py",
    "vestia-ai/requirements.txt",
    "vestia-ai/run.py"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create empty files
for file in files:
    with open(file, "w") as f:
        if file.endswith(".json"):
            f.write("[]")

print("✅ Project structure created successfully!")