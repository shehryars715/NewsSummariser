from scrap import scrape_once, check_supabase_connection
from rich.console import Console
from rich.panel import Panel
from rich import print
import time
import sys

# Initialize Rich console for pretty output
console = Console()

def main():
    """
    Main function to run the scraping process.
    """
    console.print(Panel.fit("📰 Article Scraper to Supabase", style="bold blue"))
    console.print("Starting the scraping process...\n")

    # 1. Check Database Connection First
    console.rule("Step 1: Database Connection Check")
    if not check_supabase_connection():
        console.print("\n[red]❌ Aborting. Could not establish a database connection.[/red]")
        sys.exit(1) # Exit with an error code
    console.print("[green]✅ Database connection confirmed.[/green]\n")

    # 2. Run the Scraper
    console.rule("Step 2: Scraping Articles")
    start_time = time.time() # Start a timer

    try:
        scrape_once() # This is your main scraping function
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Process interrupted by user. Exiting gracefully.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ A critical error occurred during scraping: {e}[/red]")
        # It's often helpful to see the full traceback for debugging
        import traceback
        console.print(f"[red]{traceback.format_exc()}[/red]")
        sys.exit(1)
    finally:
        # This block runs whether there was an error or not
        elapsed_time = time.time() - start_time
        console.print(f"\n[i] Total execution time: {elapsed_time:.2f} seconds[/i]")

    # 3. Conclusion
    console.rule("Complete")
    console.print("[green]✅ Scraping cycle finished.[/green]")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()