===============
Changelog
===============

2.13.0 (unreleased)
---------------------

Features
^^^^^^^^^^

* Added support for Sphinx 3.4.x and 3.5.x.
* :mod:`sphinx_toolbox.more_autodoc.autoprotocol` -- Added support for generic bases, such as ``class SupportsAbs(Protocol[T_co]): ...``.
* :mod:`sphinx_toolbox.more_autosummary` -- Added the :confval:`autosummary_col_type` configuration option.
* :func:`sphinx_toolbox.latex.replace_unknown_unicode` -- Add support for converting ``≥`` and ``≤``.


Breaking Changes
^^^^^^^^^^^^^^^^^^

* :mod:`sphinx_toolbox.flake8` -- Now requires the ``flake8`` extra to be installed (``pip install sphinx-toolbox[flake8]``)
* :mod:`sphinx_toolbox.pre_commit` -- Now requires the ``precommit`` extra to be installed (``pip install sphinx-toolbox[precommit]``)


Bugs Fixed
^^^^^^^^^^^^^

* :mod:`sphinx_toolbox.more_autosummary` -- Ensure ``__all__`` is respected for autosummary tables.


-----

.. note:: The changlog prior to 2.13.0 has not been compiled yet.
