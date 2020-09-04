# 3rd party
import pytest
from bs4 import BeautifulSoup  # type: ignore
from pytest_regressions.file_regression import FileRegressionFixture  # type: ignore

# this package
from tests.common import check_html_regression


def test_build_sphinx(sphinx_src_app):
	# app is a Sphinx application object for default sphinx project (`tests/doc-test/sphinx-test-github-root`).
	sphinx_src_app.build()
	sphinx_src_app.build()


@pytest.mark.parametrize("sphinx_source_page", ["index.html"], indirect=True)
def test_output_sphinx(sphinx_source_page: BeautifulSoup, file_regression: FileRegressionFixture):
	# Make sure the page title is what you expect
	title = sphinx_source_page.find("h1").contents[0].strip()
	assert "sphinx-toolbox Demo - Sphinx source" == title

	tag_count = 0

	for a_tag in sphinx_source_page.select("a.reference.internal"):
		if tag_count == 0:
			if a_tag.contents[0] == "sphinx_toolbox/config.py":
				assert a_tag["href"] == "_modules/sphinx_toolbox/config.html#sphinx_toolbox/config.py"
		elif tag_count == 1:
			if a_tag.contents[0] == "source code":
				assert a_tag["href"] == "_modules/sphinx_toolbox/config.html#sphinx_toolbox/config.py"
		tag_count += 1

	assert tag_count == 2

	check_html_regression(sphinx_source_page, file_regression)
