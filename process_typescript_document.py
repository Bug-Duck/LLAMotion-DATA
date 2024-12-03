import os
import glob

def read_api_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return content

def generate_ts_file():
    api_dir = "data/apis"
    output = "export const apiDocuments = {\n"
    
    # Get all .api files
    api_files = glob.glob(os.path.join(api_dir, "*.api"))
    
    for api_file in api_files:
        # Get the API name from filename (without extension)
        api_name = os.path.basename(api_file).replace('.api', '')
        
        # Read content
        content = read_api_file(api_file)
        
        # Format content for template string
        formatted_content = content.replace('`', '\\`').replace('$', '\\$')
        
        # Add to output
        output += f"  {api_name}: `{formatted_content}`,\n\n"
    
    output += "}"
    
    # Write to TypeScript file
    with open("api-documents.ts", "w") as f:
        f.write(output)

if __name__ == "__main__":
    generate_ts_file()