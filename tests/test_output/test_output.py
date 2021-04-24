# stdlib
import re
import sys
from typing import List, Union

# 3rd party
import pytest
from _pytest.mark import ParameterSet
from bs4 import BeautifulSoup  # type: ignore
from coincidence.regressions import AdvancedFileRegressionFixture
from coincidence.selectors import min_version, only_version
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList

# this package
from sphinx_toolbox.testing import HTMLRegressionFixture


def test_build_example(testing_app):
	with pytest.warns(UserWarning, match="(No codes specified|No such code 'F401')"):
		testing_app.build()
		testing_app.build()


@pytest.mark.parametrize("page", ["example.html"], indirect=True)
def test_example_html_output(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "sphinx-toolbox Demo - reST Example" == title

	selector_string = "div.body div#sphinx-toolbox-demo-rest-example"
	body = list(filter(lambda a: a != '\n', page.select(selector_string)[0].contents))[1:]

	assert len(body) == 4

	assert body[0].name == 'p'
	assert body[0]["id"] == "example-0"
	assert body[0].contents == []

	assert body[1].name == "div"
	assert body[1]["class"] == ["highlight-rest", "notranslate"]
	assert body[1].contents[0].name == "div"
	assert body[1].contents[0]["class"] == ["highlight"]

	assert body[2].name == "div"
	assert body[2]["class"] == ["highlight-python", "notranslate"]

	assert body[3].name == 'p'
	assert body[3].contents == []


pages_to_check: List[Union[str, ParameterSet]] = [
		"assets.html",
		"augment-defaults.html",
		"autodoc-ellipsis.html",
		"autonamedtuple.html",
		"autoprotocol.html",
		"autotypeddict.html",
		"code-block.html",
		"confval.html",
		"decorators.html",
		"example.html",
		"flake8.html",
		"formatting.html",
		"installation.html",
		"no_docstring.html",
		"overloads.html",
		"pre-commit.html",
		"regex.html",
		"shields.html",
		"sourcelink.html",
		"typevars.html",
		"variables.html",
		"wikipedia.html",
		"documentation-summary.html",
		"github.html",
		"collapse.html",
		pytest.param(
				"instancevar.html",
				marks=pytest.mark.skipif(
						condition=sys.version_info < (3, 7),
						reason="Output differs on Python 3.6",
						),
				),
		pytest.param(
				"generic_bases.html",
				marks=only_version(3.6, reason="Output differs on Python 3.6"),
				id="generic_bases_36"
				),
		pytest.param(
				"generic_bases.html",
				marks=only_version(3.7, reason="Output differs on Python 3.7"),
				id="generic_bases_37"
				),
		pytest.param(
				"generic_bases.html",
				marks=min_version(3.8, reason="Output differs on Python 3.8+"),
				id="generic_bases"
				),
		pytest.param(
				"autonamedtuple_pep563.html",
				marks=min_version(3.7, reason="Output differs on Python 3.6, and not as relevant."),
				id="autonamedtuple_pep563"
				),
		pytest.param(
				"genericalias.html",
				marks=min_version(3.7, reason="Output differs on Python 3.6"),
				id="genericalias"
				),
		]


def test_html_output(testing_app, html_regression: HTMLRegressionFixture):
	"""
	Parametrize new files here rather than as their own function.
	"""

	with pytest.warns(UserWarning, match="(No codes specified|No such code 'F401')"):
		testing_app.build(force_all=True)

	for page in pages_to_check:
		if isinstance(page, str):
			page = pytest.param(page, id=page)

		pagename: str = page.values[0]  # type: ignore
		page_id: str = page.id or pagename
		for mark in page.marks:
			if mark.kwargs.get("condition", False):
				if "reason" in mark.kwargs:
					print(f"Skipping {page_id!r}: {mark.kwargs['reason']}")

					break
				else:
					print(f"Skipping {page_id!r}")
					break
		else:
			print(f"Checking output for {page_id}")
			page_id = page_id.replace('.', '_').replace('-', '_')
			content = (testing_app.outdir / pagename).read_text()
			html_regression.check(BeautifulSoup(content, "html5lib"), extension=f"_{page_id}_.html")

		continue


@pytest.mark.sphinx("latex", srcdir="test-root")
def test_latex_output(app, advanced_file_regression: AdvancedFileRegressionFixture):

	assert app.builder.name.lower() == "latex"
	app.build()

	output_file = PathPlus(app.outdir / "python.tex")
	content = StringList(output_file.read_lines())
	advanced_file_regression.check(
			re.sub(r"\\date{.*}", r"\\date{Mar 11, 2021}", str(content)),
			extension=".tex",
			)
