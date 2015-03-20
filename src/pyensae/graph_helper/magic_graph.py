#-*- coding: utf-8 -*-
"""
@file
@brief Magic commands about graphs

.. versionadded:: 1.1
"""

from IPython.core.magic import magics_class, line_magic
from pyquickhelper import MagicCommandParser, MagicClassWithHelpers

# do not import a module which imports matplotlib
# if this module is imported, this class is being tested and it affects sphinx
# when it generates the documentation
from .matplotlib_helper import mpl_switch_style


@magics_class
class MagicGraph(MagicClassWithHelpers):

    """
    Defines magic commands about graphs

    .. versionadded:: 1.1
    """

    @staticmethod
    def mpl_style_parser():
        """
        defines the way to parse the magic command ``%mpl_style``
        """
        parser = MagicCommandParser(description='changes matplotlib style')
        parser.add_argument(
            'style',
            type=str,
            help='style, ggplot for exemple',
            default="ggplot")
        return parser

    @line_magic
    def mpl_style(self, line):
        """
        defines ``%mpl_style``
        which changes the style of matplotlib graphs, example: ``%mpl_style ggplot``
        """
        parser = self.get_parser(MagicGraph.mpl_style_parser, "mpl_style")
        args = self.get_args(line, parser)

        if args is not None:
            style = args.style
            mpl_switch_style(style)


def register_graph_magics():
    """
    register magics function, can be called from a notebook
    """
    from IPython import get_ipython
    ip = get_ipython()
    ip.register_magics(MagicGraph)
