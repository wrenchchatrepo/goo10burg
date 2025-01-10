import os
import typer
from typing import Optional
from rich import print
from rich.console import Console
from rich.progress import Progress

from utils.yaml_handler import YAMLHandler
from utils.gemini_api import GeminiAPI
from utils.eraser_api import EraserAPI
from utils.file_handler import FileHandler

app = typer.Typer()
console = Console()

def load_config():
    """Load application configuration"""
    config_path = "config/config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

@app.command()
async def generate(
    metadata_file: str = typer.Option(
        ...,
        "--metadata",
        "-m",
        help="Path to YAML metadata file"
    )
):
    """Generate content based on metadata"""
    try:
        config = load_config()
        
        # Initialize handlers
        yaml_handler = YAMLHandler(config)
        file_handler = FileHandler(config)
        gemini_api = GeminiAPI()
        eraser_api = EraserAPI()
        
        with Progress() as progress:
            task = progress.add_task("Processing...", total=100)
            
            # Parse metadata
            metadata = yaml_handler.parse_metadata(metadata_file)
            progress.update(task, advance=20)
            
            # Generate content
            if 'article_meta_data' in metadata:
                content = await gemini_api.generate_article_content(metadata['article_meta_data'])
                progress.update(task, advance=30)
                
                # Generate diagrams if needed
                if metadata['article_meta_data']['number_of_diagrams'] > 0:
                    diagrams = []
                    for i in range(metadata['article_meta_data']['number_of_diagrams']):
                        prompt_key = f'diagram_prompt_{i+1}'
                        diagram = eraser_api.generate_diagram(
                            metadata['article_meta_data'][prompt_key]
                        )
                        diagrams.append(diagram)
                    content['diagrams'] = diagrams
                progress.update(task, advance=25)
                
                # Save content
                output_path = file_handler.save_article(content, metadata['article_meta_data'])
                progress.update(task, advance=25)
                
                console.print(f"[green]Article saved to: {output_path}[/green]")
                
            elif 'script_metadata' in metadata:
                content = await gemini_api.generate_script_content(metadata['script_metadata'])
                progress.update(task, advance=30)
                
                # Generate diagram if needed
                if metadata['script_metadata']['number_of_diagrams'] == 1:
                    diagram = eraser_api.generate_diagram(
                        metadata['script_metadata']['diagram_prompt_1']
                    )
                    content['diagram'] = diagram
                progress.update(task, advance=25)
                
                # Save content
                output_paths = file_handler.save_script(content, metadata['script_metadata'])
                progress.update(task, advance=25)
                
                for file_type, path in output_paths.items():
                    console.print(f"[green]{file_type.capitalize()} saved to: {path}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
