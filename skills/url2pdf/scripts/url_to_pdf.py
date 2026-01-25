#!/usr/bin/env python3
"""
URL to PDF Converter

This script converts web pages to PDF files using Playwright.
It can process single URLs or batch convert multiple URLs from a file.

Usage:
    # Single URL
    python url_to_pdf.py --url "https://example.com" --output "output.pdf"

    # Batch processing from file (one URL per line)
    python url_to_pdf.py --file "urls.txt" --output-dir "./pdfs"

    # With custom options
    python url_to_pdf.py --file "urls.txt" --output-dir "./pdfs" --format A4 --landscape

Requirements:
    pip install playwright
    playwright install chromium
"""

import argparse
import sys
import os
from pathlib import Path
from urllib.parse import urlparse
import re

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright is not installed.")
    print("Please install it with: pip install playwright")
    print("Then run: playwright install chromium")
    sys.exit(1)


def sanitize_filename(url):
    """Convert URL to a safe filename"""
    # Parse the URL
    parsed = urlparse(url)

    # Use domain + path for filename
    domain = parsed.netloc.replace('www.', '')
    path = parsed.path.strip('/').replace('/', '_')

    # Create base filename
    if path:
        filename = f"{domain}_{path}"
    else:
        filename = domain

    # Remove invalid characters
    filename = re.sub(r'[^\w\-_.]', '_', filename)

    # Limit length
    if len(filename) > 100:
        filename = filename[:100]

    return f"{filename}.pdf"


def url_to_pdf(url, output_path, page_format='A4', landscape=False, timeout=30000):
    """
    Convert a single URL to PDF

    Args:
        url: The URL to convert
        output_path: Path where the PDF will be saved
        page_format: Page format (A4, Letter, etc.)
        landscape: Whether to use landscape orientation
        timeout: Page load timeout in milliseconds

    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate to URL
            print(f"Loading: {url}")
            response = page.goto(url, timeout=timeout, wait_until='networkidle')

            if not response or response.status >= 400:
                browser.close()
                return False, f"Failed to load URL (status: {response.status if response else 'unknown'})"

            # Wait a bit for dynamic content
            page.wait_for_timeout(1000)

            # Generate PDF
            print(f"Generating PDF: {output_path}")
            page.pdf(
                path=output_path,
                format=page_format,
                landscape=landscape,
                print_background=True,
                margin={
                    'top': '10mm',
                    'right': '10mm',
                    'bottom': '10mm',
                    'left': '10mm'
                }
            )

            browser.close()
            return True, None

    except Exception as e:
        return False, str(e)


def batch_convert(urls, output_dir, page_format='A4', landscape=False, timeout=30000):
    """
    Batch convert multiple URLs to PDFs

    Args:
        urls: List of URLs
        output_dir: Directory to save PDFs
        page_format: Page format (A4, Letter, etc.)
        landscape: Whether to use landscape orientation
        timeout: Page load timeout in milliseconds

    Returns:
        dict: Statistics about the conversion
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    results = {
        'total': len(urls),
        'success': 0,
        'failed': 0,
        'errors': []
    }

    for i, url in enumerate(urls, 1):
        url = url.strip()
        if not url or url.startswith('#'):
            continue

        print(f"\n[{i}/{len(urls)}] Processing: {url}")

        # Generate output filename
        filename = sanitize_filename(url)
        output_file = output_path / filename

        # Convert to PDF
        success, error = url_to_pdf(url, str(output_file), page_format, landscape, timeout)

        if success:
            results['success'] += 1
            print(f"✓ Success: {output_file}")
        else:
            results['failed'] += 1
            results['errors'].append({'url': url, 'error': error})
            print(f"✗ Failed: {error}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='Convert web pages to PDF files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single URL
  python url_to_pdf.py --url "https://example.com" --output "example.pdf"

  # Batch from file
  python url_to_pdf.py --file "urls.txt" --output-dir "./pdfs"

  # Custom format
  python url_to_pdf.py --file "urls.txt" --output-dir "./pdfs" --format Letter --landscape
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--url', help='Single URL to convert')
    input_group.add_argument('--file', help='File containing URLs (one per line)')

    # Output options
    parser.add_argument('--output', help='Output PDF file path (for single URL)')
    parser.add_argument('--output-dir', help='Output directory (for batch processing)', default='./pdfs')

    # PDF options
    parser.add_argument('--format', choices=['A4', 'Letter', 'A3', 'Legal', 'Tabloid'],
                       default='A4', help='Page format (default: A4)')
    parser.add_argument('--landscape', action='store_true', help='Use landscape orientation')
    parser.add_argument('--timeout', type=int, default=30000,
                       help='Page load timeout in milliseconds (default: 30000)')

    args = parser.parse_args()

    # Single URL mode
    if args.url:
        if not args.output:
            args.output = sanitize_filename(args.url)

        print(f"Converting URL to PDF...")
        success, error = url_to_pdf(args.url, args.output, args.format, args.landscape, args.timeout)

        if success:
            print(f"\n✓ PDF saved to: {args.output}")
            sys.exit(0)
        else:
            print(f"\n✗ Error: {error}")
            sys.exit(1)

    # Batch mode
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)

        # Read URLs from file
        with open(args.file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        if not urls:
            print("Error: No valid URLs found in file")
            sys.exit(1)

        print(f"Found {len(urls)} URLs to process")

        # Convert
        results = batch_convert(urls, args.output_dir, args.format, args.landscape, args.timeout)

        # Print summary
        print("\n" + "="*60)
        print("CONVERSION SUMMARY")
        print("="*60)
        print(f"Total URLs: {results['total']}")
        print(f"Successful: {results['success']}")
        print(f"Failed: {results['failed']}")

        if results['errors']:
            print("\nErrors:")
            for error in results['errors']:
                print(f"  • {error['url']}")
                print(f"    {error['error']}")

        print(f"\nPDFs saved to: {args.output_dir}")

        sys.exit(0 if results['failed'] == 0 else 1)


if __name__ == '__main__':
    main()
