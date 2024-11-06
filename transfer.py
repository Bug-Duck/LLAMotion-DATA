import os
import json


def process_files(data_dir):
    training_data = []

    # Walk through the data directory
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.user'):
                # Get the corresponding output file
                output_file = file.replace('.user', '.output')
                user_path = os.path.join(root, file)
                output_path = os.path.join(root, output_file)

                # Read user prompt and assistant response
                if os.path.exists(output_path):
                    with open(user_path, 'r', encoding='utf-8') as f:
                        user_content = f.read().strip()
                    with open(output_path, 'r', encoding='utf-8') as f:
                        assistant_content = f.read().strip()

                    # Create conversation entry
                    conversation = {
                        "messages": [
                            {"role": "human", "content": user_content},
                            {"role": "assistant", "content": assistant_content}
                        ]
                    }
                    training_data.append(conversation)

    return training_data


def save_jsonl(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in data:
            json_line = json.dumps(entry, ensure_ascii=False)
            f.write(json_line + '\n')


def main():
    data_dir = 'data'
    output_file = 'training_data.jsonl'

    # Process the files and generate training data
    training_data = process_files(data_dir)

    # Save to JSONL format
    save_jsonl(training_data, output_file)
    print(f"Converted {len(training_data)} conversations to {output_file}")


if __name__ == '__main__':
    main()
