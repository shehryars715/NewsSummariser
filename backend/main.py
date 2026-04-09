from src.scraper.scraper import scrape_once, check_supabase_connection, delete_old_articles
from src.app.services.faiss_store import faiss_create
from rich.console import Console
from rich.panel import Panel
from rich import print
import time
import sys

console = Console()


def run_scraping_cycle():
    console.print(Panel.fit("📰 Article Scraper to Supabase", style="bold blue"))
    console.print("Starting the scraping process...\n")

    # 1. Check Database Connection First
    console.rule("Step 1: Database Connection Check")
    if not check_supabase_connection():
        console.print("\n[red]❌ Aborting. Could not establish a database connection.[/red]")
        sys.exit(1)
    console.print("[green]✅ Database connection confirmed.[/green]\n")

    # 2. Run the Scraper
    console.rule("Step 2: Scraping Articles")
    start_time = time.time()

    try:
        scrape_once()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Process interrupted by user. Exiting gracefully.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ A critical error occurred during scraping: {e}[/red]")
        import traceback
        console.print(f"[red]{traceback.format_exc()}[/red]")
    finally:
        elapsed_time = time.time() - start_time
        console.print(f"\n[i] Total execution time: {elapsed_time:.2f} seconds[/i]")

    # 3. Delete Old Articles
    console.rule("Step 3: Deleting Old Articles")
    try:
        delete_old_articles()
    except Exception as e:
        console.print(f"[red]❌ Failed to delete old articles: {e}[/red]")

    # 4. Conclusion
    console.rule("Cycle Complete")
    console.print("[green]✅ Scraping cycle finished.[/green]\n")


if __name__ == "__main__":
    console.print("[bold blue]Starting continuous scraping every 2 hours...[/bold blue]\n")
    while True:
        run_scraping_cycle()
        faiss_create()
        console.print("[i]Waiting 2 hours before next cycle...[/i]\n")
        time.sleep(7200)
