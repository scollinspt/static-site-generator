import os
import tempfile
import unittest

from main import extract_title, generate_page, generate_pages_recursive


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_ignores_other_headings(self):
        markdown = "## Subheading\n\n# Page Title\n\nContent"
        self.assertEqual(extract_title(markdown), "Page Title")

    def test_extract_title_requires_h1(self):
        with self.assertRaises(ValueError):
            extract_title("## No title")


class TestGeneratePage(unittest.TestCase):
    def test_generate_page(self):
        with tempfile.TemporaryDirectory() as directory:
            markdown_path = os.path.join(directory, "content.md")
            template_path = os.path.join(directory, "template.html")
            destination_path = os.path.join(directory, "nested", "index.html")
            with open(markdown_path, "w") as markdown_file:
                markdown_file.write("# Test Page\n\nA **bold** paragraph.")
            with open(template_path, "w") as template_file:
                template_file.write("<title>{{ Title }}</title>{{ Content }}")

            generate_page(markdown_path, template_path, destination_path, "/")

            with open(destination_path) as destination_file:
                page = destination_file.read()
            self.assertEqual(
                page,
                "<title>Test Page</title>"
                "<div><h1>Test Page</h1><p>A <b>bold</b> paragraph.</p></div>",
            )

    def test_generate_page_uses_basepath(self):
        with tempfile.TemporaryDirectory() as directory:
            markdown_path = os.path.join(directory, "content.md")
            template_path = os.path.join(directory, "template.html")
            destination_path = os.path.join(directory, "index.html")
            with open(markdown_path, "w") as markdown_file:
                markdown_file.write("# Page\n\n[Home](/)\n\n![Image](/image.png)")
            with open(template_path, "w") as template_file:
                template_file.write("{{ Content }}")

            generate_page(
                markdown_path,
                template_path,
                destination_path,
                "/repository/",
            )

            with open(destination_path) as destination_file:
                page = destination_file.read()
            self.assertIn('href="/repository/"', page)
            self.assertIn('src="/repository/image.png"', page)

    def test_generate_pages_recursive(self):
        with tempfile.TemporaryDirectory() as directory:
            content_path = os.path.join(directory, "content")
            nested_path = os.path.join(content_path, "blog", "post")
            destination_path = os.path.join(directory, "public")
            template_path = os.path.join(directory, "template.html")
            os.makedirs(nested_path)
            with open(os.path.join(content_path, "index.md"), "w") as markdown_file:
                markdown_file.write("# Home")
            with open(os.path.join(nested_path, "index.md"), "w") as markdown_file:
                markdown_file.write("# Post")
            with open(template_path, "w") as template_file:
                template_file.write("<title>{{ Title }}</title>{{ Content }}")

            generate_pages_recursive(
                content_path, template_path, destination_path, "/"
            )

            self.assertTrue(os.path.isfile(os.path.join(destination_path, "index.html")))
            self.assertTrue(
                os.path.isfile(
                    os.path.join(destination_path, "blog", "post", "index.html")
                )
            )


if __name__ == "__main__":
    unittest.main()