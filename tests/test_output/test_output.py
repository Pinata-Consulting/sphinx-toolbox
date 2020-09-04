# 3rd party
import pytest
from bs4 import BeautifulSoup  # type: ignore
from pytest_regressions.file_regression import FileRegressionFixture  # type: ignore

# this package
from tests.common import check_html_regression


def test_build_example(testing_app):
	testing_app.build()
	testing_app.build()


@pytest.mark.parametrize("page", ["confval.html"], indirect=True)
def test_confval_html_output(page: BeautifulSoup, file_regression: FileRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "Confval" == title

	# Testing the actual content with check_html_regression
	check_html_regression(page, file_regression)


@pytest.mark.parametrize("page", ["shields.html"], indirect=True)
def test_shields_html_output(page: BeautifulSoup, file_regression: FileRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "sphinx-toolbox Demo - Shields" == title

	assert list(filter(lambda a: a != "\n",
						page.select("div.body div#sphinx-toolbox-demo-shields")[0].contents))[1:]

	# Testing the actual content with check_html_regression
	check_html_regression(page, file_regression)


@pytest.mark.parametrize("page", ["code-block.html"], indirect=True)
def test_code_html_output(page: BeautifulSoup, file_regression: FileRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "sphinx-toolbox Demo - Code" == title

	assert list(filter(lambda a: a != "\n", page.select("div.body div#sphinx-toolbox-demo-code")[0].contents))[1:]

	# Testing the actual content with check_html_regression
	check_html_regression(page, file_regression)


@pytest.mark.parametrize("page", ["example.html"], indirect=True)
def test_example_html_output(page: BeautifulSoup, file_regression: FileRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "sphinx-toolbox Demo - reST Example" == title

	body = list(
			filter(lambda a: a != "\n", page.select("div.body div#sphinx-toolbox-demo-rest-example")[0].contents)
			)[1:]

	assert len(body) == 4

	assert body[0].name == "p"
	assert body[0]["id"] == "example-0"
	assert body[0].contents == []

	assert body[1].name == "div"
	assert body[1]["class"] == ["highlight-rest", "notranslate"]
	assert body[1].contents[0].name == "div"
	assert body[1].contents[0]["class"] == ["highlight"]

	assert body[2].name == "div"
	assert body[2]["class"] == ["highlight-python", "notranslate"]

	assert body[3].name == "p"
	assert body[3].contents == []

	# Testing the actual content with check_html_regression
	check_html_regression(page, file_regression)


@pytest.mark.parametrize("page", ["installation.html"], indirect=True)
def test_installation_html_output(page: BeautifulSoup, file_regression: FileRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "sphinx-toolbox Demo - Installation" == title

	assert list(
			filter(lambda a: a != "\n", page.select("div.body div#sphinx-toolbox-demo-installation")[0].contents)
			)[1:]

	# Testing the actual content with check_html_regression
	check_html_regression(page, file_regression)


@pytest.mark.parametrize("page", ["augment-defaults.html"], indirect=True)
def test_augment_defaults_html_output(page: BeautifulSoup, file_regression: FileRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "Autodoc Augment Defaults" == title

	# Testing the actual content with check_html_regression
	check_html_regression(page, file_regression)
