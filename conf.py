# BASEDIR is set by <lang>/conf.py
"""
Use "-D language=<LANG>" option to build a localized mayavi document.
For example::

    sphinx-build -D language=ja -b html . _build/html

This conf.py do:

- Specify `locale_dirs` and `gettext_compact`.
- Overrides source directory as 'mayavi/docs/source/mayavi`.

"""
import os
from sphinx.util.pycompat import execfile_

BASEDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mayavi/docs/source/mayavi')

execfile_(os.path.join(BASEDIR, 'conf.py'), globals())

locale_dirs = [os.path.join(BASEDIR, '../../../../locale/')]
gettext_compact = False

def setup(app):
    from sphinx.ext.autodoc import cut_lines
    from sphinx.util.docfields import GroupedField
    app.srcdir = BASEDIR
    app.confdir = app.srcdir
    app.connect('autodoc-process-docstring', cut_lines(4, what=['module']))
    app.add_object_type('confval', 'confval',
                        objname='configuration value',
                        indextemplate='pair: %s; configuration value')
    fdesc = GroupedField('parameter', label='Parameters',
                         names=['param'], can_collapse=True)
    app.add_object_type('event', 'event', 'pair: %s; event', parse_event,
                        doc_field_types=[fdesc])

    # workaround for RTD
    from sphinx.util import logging
    logger = logging.getLogger(__name__)
    app.info = lambda *args, **kwargs: logger.info(*args, **kwargs)
    app.warn = lambda *args, **kwargs: logger.warning(*args, **kwargs)
    app.debug = lambda *args, **kwargs: logger.debug(*args, **kwargs)
