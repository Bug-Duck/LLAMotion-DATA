import os
import re
import json
from xml.etree import ElementTree as ET

def read_file_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_apis_from_xml(content):
    try:
        # Look for <apis> tag using regex
        match = re.search(r'<apis>(.*?)</apis>', content, re.DOTALL)
        if not match:
            return []
        
        # Parse the XML content
        xml_content = f'<root>{match.group(0)}</root>'
        root = ET.fromstring(xml_content)
        
        # Extract api filenames
        apis = []
        for api in root.findall('.//api'):
            apis.append(api.text)
        
        return apis
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return []

def process_files(base_path):
    conversations = []
    examples_path = os.path.join(base_path, "examples")
    usages_path = os.path.join(base_path, "usages")
    apis_path = os.path.join(base_path, "apis")
    
    # Get all user files from both examples and usages directories
    user_files = []
    if os.path.exists(examples_path):
        user_files.extend([os.path.join("examples", f) for f in os.listdir(examples_path) if f.endswith('.user')])
    if os.path.exists(usages_path):
        user_files.extend([os.path.join("usages", f) for f in os.listdir(usages_path) if f.endswith('.user')])
    
    for user_file in user_files:
        user_path = os.path.join(base_path, user_file)
        output_file = user_file.replace('.user', '.output')
        output_path = os.path.join(base_path, output_file)
        
        if not os.path.exists(user_path):
            print(f"User file not found: {user_path}")
            continue
            
        user_content = read_file_content(user_path)
        
        # Extract API references
        api_files = extract_apis_from_xml(user_content)
        
        # Build system message
        system_message = "You are a animation engineer and you need to use a animation engine named VueMotion to complete the task.\n\n"
        
        # Add API documentation to system message
        for api_file in api_files:
            api_path = os.path.join(apis_path, api_file)
            if os.path.exists(api_path):
                api_content = read_file_content(api_path)
                system_message += f"Documentation for {api_file}:\n"
                system_message += api_content + "\n\n"
        
        # Remove XML tags from user content
        user_content = re.sub(r'<apis>.*?</apis>\n?', '', user_content, flags=re.DOTALL).strip()
        
        # Create conversation
        conversation = {
            "messages": [
                {"role": "system", "content": system_message.strip()},
                {"role": "user", "content": user_content}
            ]
        }
        
        # Add assistant response if output file exists
        if os.path.exists(output_path):
            assistant_content = read_file_content(output_path)
            conversation["messages"].append({
                "role": "assistant",
                "content": assistant_content
            })
            conversations.append(conversation)
    
    return conversations

def main():
    # 使用绝对路径或确保运行脚本时在正确的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "data")
    
    conversations = process_files(base_path)
    
    # Save to JSON file
    output_file = "training_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"conversations": conversations}, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(conversations)} conversations and saved to {output_file}")

if __name__ == "__main__":
    main()