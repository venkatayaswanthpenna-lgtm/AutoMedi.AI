import os
import re

directory = r"e:\Automotive Technician\autorepair-ai\frontend\src"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace double quotes or single quotes containing the url
    # e.g., 'http://localhost:8000/api/v1...' -> `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1...`
    # Also handle backticks if they are already template literals.
    
    # We can just replace http://localhost:8000 literally.
    # If it's inside backticks: `http://localhost:8000/api/v1` -> `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1`
    # If it's inside single quotes: 'http://localhost:8000/api/v1' -> `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1`
    
    # First, let's normalize quotes around the URL if they are simple strings.
    # We will use regex to find 'http://localhost:8000...' and "http://localhost:8000..." and replace them with template literals.
    
    # Replace single/double quoted strings that start with http://localhost:8000
    pattern1 = r"(?:'|\")http://localhost:8000(.*?)(?:'|\")"
    content = re.sub(pattern1, r"`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}\1`", content)
    
    # Replace instances already in backticks: `http://localhost:8000...`
    pattern2 = r"`http://localhost:8000(.*?)`"
    content = re.sub(pattern2, r"`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}\1`", content)
    
    # Replace any leftover raw ones just in case
    # content = content.replace("http://localhost:8000", "${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith(('.ts', '.tsx')):
            process_file(os.path.join(root, file))

print("Replacement complete.")
