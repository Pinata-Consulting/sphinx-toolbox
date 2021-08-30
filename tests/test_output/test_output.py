# stdlib
import re
import sys
from typing import List, Union

# 3rd party
import pytest
import sphinx
from _pytest.mark import ParameterSet
from bs4 import BeautifulSoup  # type: ignore
from coincidence.params import param
from coincidence.regressions import AdvancedFileRegressionFixture
from coincidence.selectors import min_version, only_version
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from jinja2 import Template
from pytest_regressions.common import check_text_files

# this package
from sphinx_toolbox.latex import better_header_layout
from sphinx_toolbox.testing import HTMLRegressionFixture, remove_html_footer, remove_html_link_tags


def test_build_example(testing_app):
	with pytest.warns(UserWarning, match="(No codes specified|No such code 'F401')"):
		testing_app.build()
		testing_app.build()


@pytest.mark.parametrize("page", ["example.html"], indirect=True)
def test_example_html_output(page: BeautifulSoup):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "sphinx-toolbox Demo - reST Example" == title

	selector_string = "div.body div#sphinx-toolbox-demo-rest-example"

	body = list(filter(lambda a: a != '\n', page.select(selector_string)[0].contents))[1:]
	assert len(body) == 3

	assert body[0].name == 'p'
	assert body[0]["id"] == "example-0"
	assert body[0].contents == []

	assert body[1].name == "div"
	assert body[1]["class"] == ["rest-example", "docutils", "container"]

	body_body = list(filter(lambda a: a != '\n', body[1].contents))
	assert len(body_body) == 2

	assert body_body[0].name == "div"
	assert body_body[0]["class"] == ["highlight-rest", "notranslate"]

	assert body_body[0].contents[0].name == "div"
	assert body_body[0].contents[0]["class"] == ["highlight"]

	assert body_body[1].name == "div"
	assert body_body[1]["class"] == ["highlight-python", "notranslate"]

	assert body[2].name == 'p'
	assert body[2].contents == []


pages_to_check: List[ParameterSet] = [
		param("assets.html", False, idx=0),
		param("augment-defaults.html", True, idx=0),
		param("autodoc-ellipsis.html", True, idx=0),
		pytest.param(
				"autonamedtuple.html",
				True,
				marks=pytest.mark.skipif(
						condition=sys.version_info >= (3, 10),
						reason="Output differs on Python 3.10",
						),
				id="autonamedtuple.html"
				),
		pytest.param(
				"autonamedtuple.html",
				True,
				marks=min_version((3, 10), reason="Output differs on Python 3.10"),
				id="autonamedtuple_3_10",
				),
		param("autoprotocol.html", True, idx=0),
		param("autotypeddict.html", True, idx=0),
		param("code-block.html", True, idx=0),
		param("changeset.html", False, idx=0),
		param("confval.html", True, idx=0),
		param("decorators.html", True, idx=0),
		param("example.html", False, idx=0),
		param("flake8.html", False, idx=0),
		param("formatting.html", False, idx=0),
		param("installation.html", False, idx=0),
		param("no_docstring.html", True, idx=0),
		param("overloads.html", True, idx=0),
		param("pre-commit.html", False, idx=0),
		param("regex.html", True, idx=0),
		param("shields.html", False, idx=0),
		param("sourcelink.html", True, idx=0),
		param("typevars.html", True, idx=0),
		param("variables.html", True, idx=0),
		param("wikipedia.html", False, idx=0),
		param("documentation-summary.html", False, idx=0),
		param("documentation-summary-meta.html", False, idx=0),
		param("github.html", False, idx=0),
		param("latex.html", False, idx=0),
		param("collapse.html", False, idx=0),
		param("footnote_symbols.html", False, idx=0),
		param(
				"instancevar.html",
				True,
				marks=pytest.mark.skipif(
						condition=sys.version_info < (3, 7),
						reason="Output differs on Python 3.6",
						),
				idx=0,
				),
		pytest.param(
				"generic_bases.html",
				True,
				marks=only_version(3.6, reason="Output differs on Python 3.6"),
				id="generic_bases_36"
				),
		pytest.param(
				"generic_bases.html",
				True,
				marks=min_version(3.7, reason="Output differs on Python 3.8+"),
				id="generic_bases"
				),
		pytest.param(
				"autonamedtuple_pep563.html",
				True,
				marks=min_version(3.7, reason="Output differs on Python 3.6, and not as relevant."),
				id="autonamedtuple_pep563"
				),
		pytest.param(
				"genericalias.html",
				True,
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

	caught_exceptions: List[BaseException] = []

	for page in pages_to_check:
		pagename: str = page.values[0]  # type: ignore
		is_template: bool = page.values[1]  # type: ignore
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
			try:
				html_regression.check(
						BeautifulSoup(content, "html5lib"),
						extension=f"_{page_id}_.html",
						jinja2=is_template,
						)
			except BaseException as e:
				caught_exceptions.append(e)

		continue

	print(caught_exceptions)

	for exception in caught_exceptions:
		raise exception


def test_sidebar_links_output(testing_app, advanced_file_regression: AdvancedFileRegressionFixture):
	with pytest.warns(UserWarning, match="(No codes specified|No such code 'F401')"):
		testing_app.build(force_all=True)

	content = (testing_app.outdir / "index.html").read_text()

	page = BeautifulSoup(content, "html5lib")
	page = remove_html_footer(page)
	page = remove_html_link_tags(page)

	for div in page.select("script"):
		if "_static/language_data.js" in str(div):
			div.extract()

	def check_fn(obtained_filename, expected_filename):
		print(obtained_filename, expected_filename)
		expected_filename = PathPlus(expected_filename)
		template = Template(expected_filename.read_text())

		expected_filename.write_text(
				template.render(
						sphinx_version=sphinx.version_info,
						python_version=sys.version_info,
						)
				)

		return check_text_files(obtained_filename, expected_filename)

	advanced_file_regression.check(
			str(StringList(page.prettify())),
			extension=".html",
			check_fn=check_fn,
			)


class LaTeXRegressionFixture(AdvancedFileRegressionFixture):
	"""
	Subclass of :class:`pytest_regressions.file_regression.FileRegressionFixture`
	for checking LaTeX files.
	"""  # noqa: D400

	def check(  # type: ignore
		self,
		contents: Union[str, StringList],
		*,
		extension: str = ".html",
		jinja2: bool = False,
		**kwargs
		):
		r"""
		Check a LaTeX file generated by Sphinx for regressions,
		using `pytest-regressions <https://pypi.org/project/pytest-regressions/>`__

		:param contents:
		:param \*\*kwargs: Additional keyword arguments passed to
			:meth:`pytest_regressions.file_regression.FileRegressionFixture.check`.
		"""  # noqa: D400

		__tracebackhide__ = True

		def check_fn(obtained_filename, expected_filename):
			print(obtained_filename, expected_filename)
			expected_filename = PathPlus(expected_filename)

			template = Template(
					expected_filename.read_text(),
					block_start_string="<%",
					block_end_string="%>",
					variable_start_string="<<",
					variable_end_string=">>",
					comment_start_string="<#",
					comment_end_string="#>",
					)

			expected_filename.write_text(
					template.render(
							sphinx_version=sphinx.version_info,
							python_version=sys.version_info,
							)
					)

			return check_text_files(obtained_filename, expected_filename)

		return super().check(
				re.sub(r"\\date{.*}", r"\\date{Mar 11, 2021}", str(contents).replace("\\sphinxAtStartPar\n", '')),
				extension=".tex",
				check_fn=check_fn,
				)


@pytest.fixture()
def latex_regression(datadir, original_datadir, request) -> LaTeXRegressionFixture:
	"""
	Returns a :class:`~.LaTexRegressionFixture` scoped to the test function.
	"""

	return LaTeXRegressionFixture(datadir, original_datadir, request)


@pytest.mark.sphinx("latex", srcdir="test-root")
def test_latex_output(app, latex_regression: LaTeXRegressionFixture):

	assert app.builder.name.lower() == "latex"

	with pytest.warns(UserWarning, match="(No codes specified|No such code 'F401')"):
		app.build()

	output_file = PathPlus(app.outdir / "python.tex")
	latex_regression.check(StringList(output_file.read_lines()))


@pytest.mark.sphinx("latex", srcdir="test-root")
def test_latex_output_latex_layout(app, latex_regression: LaTeXRegressionFixture):

	assert app.builder.name.lower() == "latex"

	app.setup_extension("sphinx_toolbox.tweaks.latex_layout")
	app.events.emit("config-inited", app.config)

	with pytest.warns(UserWarning, match="(No codes specified|No such code 'F401')") as w:
		app.build(force_all=True)

	output_file = PathPlus(app.outdir / "python.tex")
	latex_regression.check(StringList(output_file.read_lines()))


@pytest.mark.sphinx("latex", srcdir="test-root")
def test_latex_output_better_header_layout(app, latex_regression: LaTeXRegressionFixture):

	assert app.builder.name.lower() == "latex"

	better_header_layout(app.config, 9, 19)
	app.builder.context.update(app.config.latex_elements)

	with pytest.warns(UserWarning, match="(No codes specified|No such code 'F401')") as w:
		app.build(force_all=True)

	output_file = PathPlus(app.outdir / "python.tex")
	latex_regression.check(StringList(output_file.read_lines()))


@pytest.mark.sphinx("latex", srcdir="test-root")
def test_latex_output_autosummary_col_type(app, latex_regression: LaTeXRegressionFixture):

	assert app.builder.name.lower() == "latex"
	app.config.autosummary_col_type = r"\Y"

	with pytest.warns(UserWarning, match="(No codes specified|No such code 'F401')"):
		app.build()

	output_file = PathPlus(app.outdir / "python.tex")
	latex_regression.check(StringList(output_file.read_lines()))
