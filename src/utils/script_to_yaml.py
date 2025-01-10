import os
import re
import yaml
from datetime import datetime
from src.utils.gemini_api import GeminiAPI

gemini_api = GeminiAPI()

async def get_next_unused_pk(pk_file_path):
    """Get the first unused PK from pk.yaml and mark it as used."""
    try:
        with open(pk_file_path, 'r') as f:
            content = f.read()
            pk_data = yaml.safe_load(content)
            print(f"Loaded PK data type: {type(pk_data)}")
            print(f"First few items: {pk_data[:3] if isinstance(pk_data, list) else 'Not a list'}")
            
        if not isinstance(pk_data, list):
            raise Exception("Invalid PK file format")
            
        for item in pk_data:
            if not isinstance(item, dict):
                print(f"Skipping non-dict item: {item}")
                continue
                
            # Skip items with nested pk structure
            if isinstance(item.get('pk'), (list, dict)):
                print(f"Skipping nested pk structure: {item}")
                continue
                
            # Get pk and used values
            pk_str = str(item.get('pk', '')).strip('"')
            used_str = str(item.get('used', '')).lower()
            print(f"Found PK: {pk_str}, used: {used_str}")
            
            if pk_str and (used_str == 'no' or used_str == 'false'):
                # Update the used status
                item['used'] = 'yes'
                
                # Write back to file preserving format
                with open(pk_file_path, 'w') as f:
                    f.write('# Available pk\'s\n')  # Preserve header
                    yaml.dump(pk_data, f, sort_keys=False, indent=2)
                    
                return pk_str
                
        raise Exception("No unused PKs available")
    except Exception as e:
        print(f"Error getting next unused PK: {e}")
        raise

async def analyze_script_with_llm(script_content, labels_file_path):
    """Use LLM to analyze script and generate metadata."""
    try:
        # Load available labels
        with open(labels_file_path, 'r') as f:
            labels_data = yaml.safe_load(f)
            available_labels = labels_data.get('labels', [])
            labels_str = '\n'.join(available_labels)

        prompt = f"""Analyze this Python script and provide the following details in a concise way:

1. A one-sentence description of what the script does
2. A one-sentence objective/purpose
3. A one-sentence description of input parameters
4. A one-sentence description of output parameters
5. Select between 1 to 5 most relevant labels from this list. Only use labels from this list and include the # symbol:
{labels_str}

Script content:
{script_content}

Important: Choose between 1 to 5 labels that are most relevant to the script's purpose. Only use labels from the provided list.

Format your response as raw YAML without any markdown formatting. Start with --- and use proper YAML formatting. Example format:

---
description: A description here
objective: An objective here
input: Input description here
output: Output description here
labels:
  - #label1
  - #label2

Your response:"""

        response = await gemini_api.generate_text(prompt)
        
        try:
            # Extract just the YAML part starting from --- and remove any markdown formatting
            yaml_content = response[response.find('---'):]
            # Remove markdown code block syntax
            yaml_content = yaml_content.replace('```yaml', '').replace('```', '')
            # Remove any leading/trailing whitespace
            yaml_content = yaml_content.strip()
            metadata = yaml.safe_load(yaml_content)
            
            # Validate and clean up labels
            if 'labels' in metadata:
                if not isinstance(metadata['labels'], list):
                    metadata['labels'] = []
                # Remove any null values and ensure we have valid labels
                metadata['labels'] = [label for label in metadata['labels'] if label and isinstance(label, str) and label.startswith('#')]
                # Ensure we have at least one label
                if not metadata['labels']:
                    metadata['labels'] = ['#script']  # Default label
            else:
                metadata['labels'] = ['#script']  # Default label
                
            return metadata
        except yaml.YAMLError:
            print(f"Error parsing LLM response as YAML: {response}")
            raise
            
    except Exception as e:
        print(f"Error analyzing script with LLM: {e}")
        raise

async def generate_yaml_from_scripts(scripts_dir, output_yaml_path):
    """Generate YAML entries from script files in the specified directory."""
    try:
        print("Starting script to YAML conversion...")
        
        if not os.path.exists(scripts_dir):
            raise Exception(f"Scripts directory not found: {scripts_dir}")
            
        # Get all Python files in the scripts directory
        script_files = [f for f in os.listdir(scripts_dir) if f.endswith('.py')]
        
        # Load existing YAML entries if the file exists
        existing_entries = []
        if os.path.exists(output_yaml_path):
            with open(output_yaml_path, 'r') as f:
                existing_entries = yaml.safe_load(f) or []
                
        # Get list of scripts that already have entries
        processed_scripts = {entry.get('existing_filename') for entry in existing_entries}
        
        # Filter to only process new scripts
        new_script_files = [f for f in script_files if f not in processed_scripts]
        total_new = len(new_script_files)
        print(f"Found {len(script_files)} Python files, {total_new} new to process")
        
        # Start with existing entries
        yaml_entries = existing_entries
        processed_count = 0
        
        for filename in new_script_files:
            try:
                print(f"Processing {filename}...")
                script_path = os.path.join(scripts_dir, filename)
                
                # Read script content
                with open(script_path, 'r') as f:
                    script_content = f.read()
                
                # Get PKs for script and diagram
                script_pk = await get_next_unused_pk('src/templates/pk.yaml')
                diagram_pk = await get_next_unused_pk('src/templates/pk.yaml')
                
                # Get LLM analysis
                llm_metadata = await analyze_script_with_llm(
                    script_content,
                    'src/templates/labels.yaml'
                )
                
                # Construct metadata
                metadata = {
                    'author': 'dion@wrench.chat',
                    'tagline_required': '1',
                    'update_date': datetime.now().strftime('%-m/%-d/%Y'),
                    'version': '1',
                    'existing_filename': filename,
                    'new_filename': filename,
                    'new_filepath': 'source_files/scripts',
                    'old_filepath': 'source_files/scripts',
                    'generated': 'false',
                    'type': 'script',
                    'pk': script_pk,
                    'number_of_diagrams': '1',
                    'diagram_1_pk': diagram_pk,
                    'language': 'python'
                }
                
                # Add LLM-generated metadata
                metadata.update(llm_metadata)
                
                yaml_entries.append(metadata)
                processed_count += 1
                print(f"Progress: {processed_count}/{total_new} new files processed")
                
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                import traceback
                print(traceback.format_exc())
                continue
        
        # Write YAML entries
        print("Writing YAML output...")
        with open(output_yaml_path, 'w') as f:
            yaml.dump(yaml_entries, f, sort_keys=False, indent=2)
        
        print(f"Successfully generated YAML at {output_yaml_path}")
        return yaml_entries
        
    except Exception as e:
        print(f"Error in generate_yaml_from_scripts: {e}")
        import traceback
        print(traceback.format_exc())
        raise

def main():
    """Main entry point for the script."""
    import argparse
    parser = argparse.ArgumentParser(description='Generate YAML metadata for Python scripts')
    parser.add_argument('--scripts-dir', default='source_files/scripts',
                      help='Directory containing Python scripts (default: source_files/scripts)')
    parser.add_argument('--output', default='source_files/yaml/script.yaml',
                      help='Output YAML file path (default: source_files/yaml/script.yaml)')
    args = parser.parse_args()

    try:
        print("Starting script to YAML conversion...")
        import asyncio
        asyncio.run(generate_yaml_from_scripts(args.scripts_dir, args.output))
        print("Conversion completed successfully")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print(traceback.format_exc())
        exit(1)

if __name__ == '__main__':
    main()
