import os
import yaml
import subprocess
import json
import asyncio
import httpx
from src.utils.eraser_api import EraserAPI
from src.utils.gemini_api import GeminiAPI
from src.config import config

gemini_api = GeminiAPI()

async def generate_files():
    """
    Generates markdown and script files from YAML configurations.
    """
    try:
        print("Starting generator...")
        yaml_dir = "source_files/yaml"
        print(f"Looking for YAML files in {yaml_dir}")
        yaml_files = [f for f in os.listdir(yaml_dir) if f.endswith(".yaml")]
        total_files = len(yaml_files)
        print(f"Found {total_files} YAML files to process: {yaml_files}")
        
        processed_count = 0
        for filename in yaml_files:
            if filename.endswith(".yaml"):
                file_path = os.path.join(yaml_dir, filename)
                with open(file_path, 'r') as yaml_file:
                    try:
                        data = yaml.safe_load(yaml_file)
                        print(f"Processing {filename}...")
                        if filename == "diagram.yaml":
                            print("Processing diagrams...")
                            for diagram in data["diagrams"]:
                                if str(diagram.get("generated")).lower() == "false":
                                    print(f"Generating diagram: {diagram.get('new_filename')}")
                                    await generate_diagram(diagram)
                                    diagram["generated"] = "yes"
                                    processed_count += 1
                                    print(f"Progress: {processed_count}/{total_files} files processed")
                        elif isinstance(data, list):
                            print(f"Found list data in {filename}")
                            for item in data:
                                print(f"Checking item in {filename}: generated = {item.get('generated')}")
                                generated = str(item.get("generated")).lower()
                                if generated == "false":
                                    if filename == "markdown.yaml":
                                        await generate_markdown(item)
                                    elif filename == "script.yaml":
                                        await generate_script(item)
                                    item["generated"] = "yes"
                                    processed_count += 1
                                    print(f"Progress: {processed_count}/{total_files} files processed")
                        elif isinstance(data, dict):
                            print(f"Found dict data in {filename}")
                            print(f"Checking dict in {filename}: generated = {data.get('generated')}")
                            generated = str(data.get("generated")).lower()
                            if generated == "false":
                                if filename == "markdown.yaml":
                                    await generate_markdown(data)
                                elif filename == "script.yaml":
                                    await generate_script(data)
                                data["generated"] = "yes"
                                processed_count += 1
                                print(f"Progress: {processed_count}/{total_files} files processed")
                        with open(file_path, 'w') as yaml_file:
                            yaml.dump(data, yaml_file, indent=2)
                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML file {filename}: {e}")
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")
                        import traceback
                        print(traceback.format_exc())
    except Exception as e:
        print(f"Error in generate_files: {e}")
        import traceback
        print(traceback.format_exc())

async def generate_markdown(config):
    """
    Generates a markdown file from a YAML configuration using Gemini.
    """
    # Extract all parameters from config
    new_filename = config.get("new_filename")
    new_filepath = config.get("new_filepath")
    old_filepath = config.get("old_filepath")
    existing_filename = config.get("existing_filename")
    description = config.get("description")
    author = config.get("author")
    approx_total_words = config.get("approx_total_words", "500")
    approx_words_per_paragraphs = config.get("approx_words_per_paragraphs", "250")
    assertion_1_sentence = config.get("assertion_1_sentence", "")
    assertion_2_sentence = config.get("assertion_2_sentence", "")
    concluding_paragraph = config.get("concluding_paragraph", "0")
    intro_paragraph = config.get("intro_paragraph", "0")
    labels = config.get("labels")
    number_assertions = config.get("number_assertions", "0")
    number_of_diagrams = config.get("number_of_diagrams", "0")
    paragraph_per_assertions = config.get("paragraph_per_assertions", "1")
    tagline_required = config.get("tagline_required")
    total_paragraphs = config.get("total_paragraphs", "1")
    update_date = config.get("update_date")
    version = config.get("version")
    diagram_1_pk = config.get("diagram_1_pk")

    front_matter = f"""---
author: {author}
tagline_required: {tagline_required}
update_date: {update_date}
version: {version}
---
"""
    # Get existing content if available
    existing_content = ""
    if existing_filename and old_filepath:
        try:
            with open(os.path.join(old_filepath, existing_filename), 'r') as old_file:
                existing_content = old_file.read()
                print(f"Found existing content in {existing_filename}")
        except FileNotFoundError:
            print(f"No existing file found at {old_filepath}/{existing_filename}")

    prompt = f"""{front_matter}
Generate markdown content for a document titled '{new_filename}' with the following specifications:

Previous version content to reference:
{existing_content if existing_content else "No previous version available"}

- Description: {description}
- Total words: approximately {approx_total_words}
- Words per paragraph: approximately {approx_words_per_paragraphs}
- Total paragraphs: {total_paragraphs}
- Include introduction paragraph: {intro_paragraph == '1'}
- Include concluding paragraph: {concluding_paragraph == '1'}

Key assertions to include:
{f'1. {assertion_1_sentence}' if assertion_1_sentence else ''}
{f'2. {assertion_2_sentence}' if assertion_2_sentence else ''}

Structure:
- Number of assertions: {number_assertions}
- Paragraphs per assertion: {paragraph_per_assertions}
- Number of diagrams referenced: {number_of_diagrams}

Labels to include:
{labels}
"""
    print(f"Generating markdown content for {new_filename}...")
    content = await gemini_api.generate_text(prompt)
    if new_filename and new_filepath and content:
        print(f"Content generated, writing to file...")
        file_path = os.path.join(new_filepath, new_filename)
        with open(file_path, 'w') as md_file:
            md_file.write(content)
        print(f"Generated markdown file: {file_path}")
        if diagram_1_pk:
            await generate_diagram(config)
            with open(file_path, 'a') as md_file:
                md_file.write(f"\n# diagram_pk: {diagram_1_pk}")

async def generate_script(config):
    """
    Generates a script file from a YAML configuration using Gemini.
    """
    new_filename = config.get("new_filename")
    new_filepath = config.get("new_filepath")
    old_filepath = config.get("old_filepath")
    description = config.get("description")
    author = config.get("author")
    objective = config.get("objective")
    input_params = config.get("input")
    output_params = config.get("output")
    language = config.get("language")
    labels = config.get("labels")
    existing_filename = config.get("existing_filename")
    tagline_required = config.get("tagline_required")
    update_date = config.get("update_date")
    version = config.get("version")
    diagram_1_pk = config.get("diagram_1_pk")
    diagram_prompt_1 = config.get("diagram_prompt_1")

    front_matter = f"""# author: {author}
# tagline_required: {tagline_required}
# update_date: {update_date}
# version: {version}
"""
    
    if existing_filename and old_filepath:
        try:
            with open(os.path.join(old_filepath, existing_filename), 'r') as old_file:
                existing_content = old_file.read()
        except FileNotFoundError:
            existing_content = ""
    else:
        existing_content = ""

    prompt = f"""{front_matter}
Generate script content for a script named '{new_filename}'. The script should have the following description: '{description}'. The objective is '{objective}'. The input parameters are '{input_params}'. The output parameters are '{output_params}'. The language is '{language}'. The following labels should be included: '{labels}'. Here is the content of an existing script that may be helpful:
{existing_content}
"""
    print(f"Generating script content for {new_filename}...")
    content = await gemini_api.generate_text(prompt)
    if new_filename and new_filepath and content:
        print(f"Content generated, writing to file...")
        file_path = os.path.join(new_filepath, new_filename)
        with open(file_path, 'w') as script_file:
            script_file.write(content)
        print(f"Generated script file: {file_path}")
        if diagram_prompt_1 and diagram_1_pk:
            await generate_diagram(config)
            with open(file_path, 'a') as script_file:
                script_file.write(f"\n# diagram_pk: {diagram_1_pk}")


async def generate_diagram(config):
    """
    Generates a diagram file from a YAML configuration using the Eraser API.
    """
    new_filename = config.get("new_filename")
    new_filepath = config.get("new_filepath")
    text = config.get("text")
    if new_filename and new_filepath and text:
        print(f"Generating diagram for {new_filename}...")
        eraser_api = EraserAPI()
        diagram_data = eraser_api.get_diagram(text)
        if diagram_data and diagram_data.get("imageUrl"):
            image_url = diagram_data.get("imageUrl")
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(image_url)
                    response.raise_for_status()
                    file_path = os.path.join(new_filepath, new_filename)
                    with open(file_path, 'wb') as image_file:
                        image_file.write(response.content)
                    print(f"Generated diagram file: {file_path}")
            except httpx.HTTPError as e:
                print(f"Error fetching diagram image: {e}")
        else:
            print(f"Could not generate diagram for {new_filename}")

if __name__ == "__main__":
    try:
        print("Starting main...")
        asyncio.run(generate_files())
        print("Generator completed successfully")
    except Exception as e:
        print(f"Error in main: {e}")
        import traceback
        print(traceback.format_exc())
