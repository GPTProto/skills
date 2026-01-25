---
name: url2pdf
description: Convert web pages to PDF files. Use this skill when users need to convert single or batch URLs to PDF format, save web content as PDF documents, or archive web pages. Triggers include requests like "convert this URL to PDF", "save these websites as PDF", "batch convert URLs to PDF", or providing a list of URLs to be converted.
---

# URL2PDF

## Overview

The URL2PDF skill enables automated conversion of web pages to PDF files. It supports both single URL conversion and batch processing of multiple URLs, making it ideal for archiving web content, creating offline documentation, or generating PDF reports from web sources.

## Quick Start

### Single URL Conversion

Convert a single web page to PDF:

```bash
python scripts/url_to_pdf.py --url "https://example.com" --output "example.pdf"
```

### Batch Conversion

Process multiple URLs from a text file (one URL per line):

```bash
python scripts/url_to_pdf.py --file urls.txt --output-dir ./pdfs
```

## Installation

Before using this skill, ensure the required dependencies are installed:

```bash
# Install Python dependencies
pip install -r scripts/requirements.txt

# Install Chromium browser for Playwright
playwright install chromium
```

## Usage Patterns

### Pattern 1: User Provides URLs in Message

When a user provides URLs directly in their message:

1. Extract the URLs from the user's message
2. Create a temporary text file with one URL per line
3. Run the batch conversion script
4. Report the results to the user

Example user request:
```
Convert these URLs to PDF:
https://example.com
https://docs.python.org
https://github.com/anthropics
```

Implementation:
```bash
# Create temporary URL file
cat > /tmp/urls.txt << 'EOF'
https://example.com
https://docs.python.org
https://github.com/anthropics
EOF

# Convert to PDFs
python scripts/url_to_pdf.py --file /tmp/urls.txt --output-dir ./pdfs
```

### Pattern 2: User Provides URL File

When a user provides a file path containing URLs:

```bash
python scripts/url_to_pdf.py --file /path/to/urls.txt --output-dir ./output
```

### Pattern 3: Single URL with Custom Filename

```bash
python scripts/url_to_pdf.py --url "https://example.com/article" --output "my-article.pdf"
```

### Pattern 4: Custom Page Format

For different paper sizes or orientations:

```bash
# A4 landscape
python scripts/url_to_pdf.py --file urls.txt --output-dir ./pdfs --format A4 --landscape

# US Letter format
python scripts/url_to_pdf.py --file urls.txt --output-dir ./pdfs --format Letter

# Legal size
python scripts/url_to_pdf.py --file urls.txt --output-dir ./pdfs --format Legal
```

## Script Reference

### url_to_pdf.py

The main conversion script with the following options:

**Input Options (choose one):**
- `--url URL` - Convert a single URL
- `--file FILE` - Convert multiple URLs from a file (one per line)

**Output Options:**
- `--output PATH` - Output file path (for single URL mode)
- `--output-dir DIR` - Output directory (for batch mode, default: ./pdfs)

**PDF Options:**
- `--format FORMAT` - Page format: A4, Letter, A3, Legal, Tabloid (default: A4)
- `--landscape` - Use landscape orientation (default: portrait)
- `--timeout MS` - Page load timeout in milliseconds (default: 30000)

**URL File Format:**

The URL file should contain one URL per line. Lines starting with `#` are treated as comments and ignored.

Example:
```
# News sites
https://news.ycombinator.com
https://www.bbc.com/news

# Documentation
https://docs.python.org
https://www.typescriptlang.org/docs/
```

**Output Filenames:**

In batch mode, PDF filenames are automatically generated from URLs:
- Domain name + path components
- Invalid characters replaced with underscores
- Limited to 100 characters
- Example: `example.com_article_page.pdf`

## Error Handling

The script handles common errors gracefully:

1. **Failed page loads** - Reports HTTP status codes and continues with remaining URLs
2. **Timeouts** - Configurable timeout with `--timeout` option
3. **Invalid URLs** - Skips invalid entries and continues processing
4. **Missing dependencies** - Clear error messages with installation instructions

After batch conversion, a summary is displayed showing:
- Total URLs processed
- Successful conversions
- Failed conversions with error details

## Best Practices

1. **Large batches** - For processing many URLs, increase timeout if pages are slow to load
2. **Dynamic content** - The script waits 1 second after page load for JavaScript to execute
3. **File organization** - Use descriptive output directory names for different projects
4. **Error recovery** - Check the conversion summary for failed URLs and retry if needed
5. **Disk space** - Ensure sufficient disk space for PDFs (especially for media-heavy pages)

## Workflow

When a user requests URL to PDF conversion:

1. **Identify the URLs**
   - Extract URLs from user message or file path
   - Validate URL format

2. **Prepare the conversion**
   - Create URL list file if needed
   - Determine output location
   - Choose appropriate format options

3. **Execute the conversion**
   - Run the script with appropriate parameters
   - Monitor for errors

4. **Report results**
   - Inform user of successful conversions
   - Report any failures with error details
   - Provide location of generated PDFs

## Example Workflows

### Workflow 1: Quick Single Page Archive

User: "Save this page as PDF: https://example.com/article"

```bash
python scripts/url_to_pdf.py --url "https://example.com/article" --output "article.pdf"
```

### Workflow 2: Documentation Set

User: "Convert all these documentation pages to PDF"

```bash
# Create URL list
cat > docs_urls.txt << 'EOF'
https://docs.site.com/getting-started
https://docs.site.com/api-reference
https://docs.site.com/tutorials
EOF

# Convert with A4 format
python scripts/url_to_pdf.py --file docs_urls.txt --output-dir ./documentation_pdfs --format A4
```

### Workflow 3: Landscape Reports

User: "Convert these dashboard URLs to landscape PDFs"

```bash
python scripts/url_to_pdf.py --file dashboard_urls.txt --output-dir ./reports --format Letter --landscape
```

## Troubleshooting

**Issue: "playwright is not installed"**
```bash
pip install playwright
playwright install chromium
```

**Issue: Timeout errors on slow pages**
```bash
# Increase timeout to 60 seconds
python scripts/url_to_pdf.py --file urls.txt --output-dir ./pdfs --timeout 60000
```

**Issue: PDFs missing content**
- Some pages require more time for JavaScript. The script includes a 1-second wait, but complex pages may need the timeout increased.
- Some pages may block headless browsers. This is rare but possible.

**Issue: Large file sizes**
- PDF sizes depend on page content (images, fonts, etc.)
- Consider the `--format` option to adjust page dimensions
- No built-in compression, but PDFs can be post-processed with other tools if needed
