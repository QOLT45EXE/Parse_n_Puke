import json #pip install jsons
import zipfile #pip install zipfile36
from pathlib import Path #pip install pathlib
from datetime import datetime #pip install datetime 

# vrrrrrrrrrrp...
def unzip_that_shit(zip_path, extract_to="exported_chats"):
    extract_path = Path(extract_to)
    extract_path.mkdir(exist_ok = True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(f"Unzipped and equipped @ {extract_path.resolve()}")
    return extract_path / "conversations.json"

# Loot JSON
def load_them_chats(json_path):
    with open(json_path, 'r', encoding = 'utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and "mapping" in data:
        return data['mapping']
    elif isinstance(data, list):
        return{str(i): entry for i, entry in enumerate(data)}
    else:
        raise ValueError("JSON structure is wrong.")

# Sniff out chats
def search_them_chats(chats, keywords):
    results = []
    for chat_id, chat_data in chats.items():
        mapping = chat_data.get('mapping', {})
        for node_id, node_data in mapping.items():
            message = node_data.get('message')
            if message and message.get('content') and message['content'].get('parts'):
                parts = message['content']['parts']
                if parts and parts[0]: 
                    text = parts[0] if isinstance(parts[0], str) else ""
                    if any(keyword.lower() in text.lower() for keyword in keywords):
                        results.append({
                            'id': node_id,
                            'text': text
                        })
    return results

# Export the goods
def export_export_read_all_about_it(results, output_file):
    with open(output_file, 'w', encoding = 'utf-8') as f:
        for i, result in enumerate(results, start = 1):
            f.write(f"--- Chatty Cathy #{i} ---\n")
            f.write(f"ID: {result['id']}\n")
            f.write(f"Message: \n{result['text']}\n")
            f.write(f"\n\n")
    print(f"Exported {len(results)} to {output_file}")

# get the party started
def main():
    zip_path = input("Enter path: ").strip()
    json_path = unzip_that_shit(zip_path)
    chats = load_them_chats(json_path)
    keywords_input = input("Slap them keywords in, separate with commas: ").strip()
    keywords = [kw.strip() for kw in keywords_input.split(',')]
    results = search_them_chats(chats, keywords)
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"chat_search_results_{timestamp}.txt"
        export_export_read_all_about_it(results, output_file)
    else:
        print("Nada, son. Try again.")

if __name__ == "__main__":
    main()