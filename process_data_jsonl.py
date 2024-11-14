import os
import re
import json
from xml.etree import ElementTree as ET

def read_file_content(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_apis_from_xml(content):
    try:
        # 使用正则表达式直接匹配所有 api 标签
        apis = re.findall(r'<api>(.*?)</api>', content, re.DOTALL)
        return [api.strip() for api in apis if api.strip()]
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
        
        # Add API documentation to system message only if API file exists
        for api_file in api_files:
            api_path = os.path.join(apis_path, api_file)
            if os.path.exists(api_path):
                api_content = read_file_content(api_path)
                system_message += f"Documentation for {api_file}:\n{api_content}\n\n"
            else:
                print(f"Warning: API file not found: {api_file}")
        
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
        
        # Always add the conversation, even if there's no output file
        conversations.append(conversation)
    
    return conversations

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "data")
    
    conversations = process_files(base_path)
    
    # Save to JSONL file
    output_file = "training_data.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for conv in conversations:
            # Write each conversation as a separate line
            f.write(json.dumps(conv, ensure_ascii=False) + '\n')
    
    print(f"Processed {len(conversations)} conversations and saved to {output_file}")

if __name__ == "__main__":
    main()