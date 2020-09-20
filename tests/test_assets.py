# this package
from sphinx_toolbox import assets
from sphinx_toolbox.testing import run_setup


def test_setup():
	setup_ret, directives, roles, additional_nodes, app = run_setup(assets.setup)

	assert roles == {"asset": assets.asset_role}
	assert additional_nodes == {assets.AssetNode}

	assert app.registry.translation_handlers == {
			"html": {"AssetNode": (assets.visit_asset_node, assets.depart_asset_node), }
			}

	assert app.config.values["assets_dir"] == ("./assets", "env", [str])
	assert app.registry.source_parsers == {}
