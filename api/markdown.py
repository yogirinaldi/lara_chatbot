import markdown2

# Some example Markdown text
markdown_text = """
#This is a heading And this is a paragraph"""

# Convert the Markdown text to HTML
html = markdown2.markdown(markdown_text)

# Print the generated HTML
print(html)