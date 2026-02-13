Contributor Guide
=================

Thank you for your interest in improving this project.
This project is open-source under the `MIT license`_ and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- `Source Code`_
- `Documentation`_
- `Issue Tracker`_
- `Code of Conduct`_

.. _MIT license: https://opensource.org/licenses/MIT
.. _Source Code: https://github.com/AnthonyTechnologies/python-xltektools
.. _Documentation: https://python-xltektools.readthedocs.io/
.. _Issue Tracker: https://github.com/AnthonyTechnologies/python-xltektools/issues

Reporting Bugs
--------------

Report bugs on the `Issue Tracker`_.

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.


Requesting Features
-------------------

Request features on the `Issue Tracker`_.


Development Environment Setup
------------------------------

You need Python 3.14+ and the following tools:

- Nox_

Install the package with development requirements:

.. code:: console

   $ pip install -e .[dev]

You can now run an interactive Python session:

.. code:: console

   $ python

.. _Nox: https://nox.thea.codes/


Project Tools
-------------

This project uses several tools to ensure code quality and consistency.

- **Nox**: A flexible test automation tool.
- **uv**: A fast Python package installer and resolver.
- **pre-commit**: A framework for managing and maintaining multi-language pre-commit hooks.
- **mypy**: Optional static typing for Python.
- **pytest**: The pytest framework makes it easy to write small tests.
- **coverage**: Code coverage measurement for Python.
- **typeguard**: Run-time type checker for Python.
- **xdoctest**: A rewrite of the standard library doctest module.
- **Sphinx**: Python documentation generator.

Testing the Project
-------------------

This project uses `Nox`_ for test automation. It orchestrates testing, linting, and documentation building across different environments.

Run the full default test suite (creates new virtual environments):

.. code:: console

   $ nox

List the available Nox sessions:

.. code:: console

   $ nox --list-sessions

Nox Sessions
~~~~~~~~~~~~

The Nox sessions are categorized into two main groups based on how they run:

New Environments
^^^^^^^^^^^^^^^^

These sessions create isolated virtual environments for each run. This ensures that tests run in a clean, reproducible state with the exact dependencies specified for the project. These are the default sessions.

**Tag:** ``new_venv``

- ``tests``: Run the test suite using pytest.
- ``mypy``: Run static type checking.
- ``typeguard``: Run runtime type checking.
- ``xdoctest``: Run doctests.
- ``docs-build``: Build the documentation.
- ``pre-commit``: Run pre-commit hooks.
- ``coverage``: Produce coverage reports.

Active Environment
^^^^^^^^^^^^^^^^^^

These sessions run tools in the currently active Python environment. This is useful for testing with different dependencies (e.g., experimental versions) or for faster iteration if you already have valid dependencies installed.

**Tag:** ``active_venv``

- ``tests_active``
- ``mypy_active``
- ``typeguard_active``
- ``xdoctest_active``
- ``docs-build_active``
- ``pre-commit_active``
- ``coverage_active``

Running Specific Sessions
~~~~~~~~~~~~~~~~~~~~~~~~~

You can run individual sessions by name:

.. code:: console

   $ nox -s tests

Or run a group of sessions using tags:

.. code:: console

   $ nox -t new_venv
   $ nox -t active_venv

Submitting Changes
------------------

Open a `pull request`_ to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

To run linting and code formatting checks before committing your change, you can install pre-commit as a Git hook by running the following command:

.. code:: console

   $ nox --session=pre-commit -- install

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

.. _pull request: https://github.com/AnthonyTechnologies/python-xltektools/pulls
.. github-only
.. _Code of Conduct: CODE_OF_CONDUCT.rst
