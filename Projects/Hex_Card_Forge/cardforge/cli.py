"""
Card Forge CLI entry point
"""

import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

app = typer.Typer(help="Card Forge - Hex Card Metadata Creator")
console = Console()


def hello_world() -> str:
    """Return a greeting message (for testing purposes).
    
    Returns:
        str: A greeting message
    """
    return "Hello, Card Forge!"


def display_title_screen() -> None:
    """Display the title screen with menu options."""
    # Create the title banner
    title = Text("CARD FORGE v1.1", style="bold magenta")
    console.print(Panel(title, box=box.DOUBLE, expand=False, border_style="magenta"))
    
    # Display menu options
    console.print(Panel(
        "\n".join([
            "[bold cyan]1.[/bold cyan] Create New Card",
            "[bold cyan]2.[/bold cyan] Import Cards",
            "[bold cyan]3.[/bold cyan] Create Booster Pack",
            "[bold cyan]4.[/bold cyan] Design Template",
            "[bold cyan]5.[/bold cyan] Add Image to Card",
            "[bold cyan]0.[/bold cyan] Exit",
        ]),
        box=box.SIMPLE,
        expand=False,
        border_style="cyan"
    ))


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Card Forge - Create customizable hex-shaped cards with metadata"""
    # If no subcommand was invoked, display the title screen
    if ctx.invoked_subcommand is None:
        display_title_screen()


@app.command("new")
def new_card() -> None:
    """Create a new card using the interactive wizard."""
    from cardforge.wizard import create_new_card
    
    console.print("[bold green]Creating new card...[/bold green]")
    
    # Custom print function to use rich console
    def rich_print(text):
        console.print(text)
    
    # Run the wizard and get the created card
    try:
        card, create_another = create_new_card(input_func=input, print_func=rich_print)
        
        if card:
            console.print(f"\n[bold green]Card '{card.title}' created![/bold green]")
            
            # Here we would save the card or add it to a session
            # This will be implemented in a future step when we add persistence
            
            if create_another:
                # Recursively call new_card to create another card
                new_card()
    except Exception as e:
        console.print(f"\n[bold red]Error creating card: {e}[/bold red]")
        if typer.confirm("Would you like to try again?"):
            new_card()


@app.command("import")
def import_cards(zip_path: str) -> None:
    """Import cards from a ZIP file."""
    # This will be implemented in a future step
    console.print(f"[bold green]Importing cards from {zip_path}...[/bold green]")
    console.print("[yellow]This feature is not yet implemented.[/yellow]")


@app.command("booster")
def create_booster() -> None:
    """Create a booster pack from multiple cards."""
    # This will be implemented in a future step
    console.print("[bold green]Creating booster pack...[/bold green]")
    console.print("[yellow]This feature is not yet implemented.[/yellow]")


@app.command("template")
def design_template() -> None:
    """Design a card template."""
    # This will be implemented in a future step
    console.print("[bold green]Designing card template...[/bold green]")
    console.print("[yellow]This feature is not yet implemented.[/yellow]")


@app.command("image")
def add_image(card_id: str, image_path: str) -> None:
    """Add an image to an existing card."""
    # This will be implemented in a future step
    console.print(f"[bold green]Adding image to card {card_id}...[/bold green]")
    console.print("[yellow]This feature is not yet implemented.[/yellow]")


if __name__ == "__main__":
    app()
