import os

def load_files(base_path):
    documents = []

    print("📥 Scanning:", base_path)

    for root, _, files in os.walk(base_path):
        print("➡️ ROOT:", root, "FILES:", files)

        for file in files:
            if file.endswith(".txt"):

                full_path = os.path.join(root, file)

                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract category from folder structure
                relative_path = full_path.replace(base_path, "")
                parts = relative_path.strip(os.sep).split(os.sep)

                category = parts[0] if len(parts) > 0 else "general"

                documents.append({
                    "text": content,
                    "file_name": file,
                    "category": category,
                    "path": full_path
                })

    return documents