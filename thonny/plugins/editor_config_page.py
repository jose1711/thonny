import tkinter as tk
from logging import getLogger
from tkinter import ttk

from thonny import get_shell, get_workbench
from thonny.config_ui import ConfigurationPage
from thonny.languages import tr
from thonny.ui_utils import ems_to_pixels

logger = getLogger(__name__)


class EditorConfigurationPage(ConfigurationPage):
    def __init__(self, master):
        ConfigurationPage.__init__(self, master)

        group_spacing = ems_to_pixels(2)

        try:
            self.add_checkbox(
                "view.name_highlighting", tr("Highlight matching names"), columnspan=2
            )
        except Exception:
            # name matcher may have been disabled
            logger.warning("Couldn't create name matcher checkbox")

        try:
            self.add_checkbox(
                "view.locals_highlighting", tr("Highlight local variables"), columnspan=2
            )
        except Exception:
            # locals highlighter may have been disabled
            logger.warning("Couldn't create name locals highlighter checkbox")

        self.add_checkbox("view.paren_highlighting", tr("Highlight parentheses"), columnspan=2)
        self.add_checkbox("view.syntax_coloring", tr("Highlight syntax elements"), columnspan=2)
        self.add_checkbox("view.highlight_tabs", tr("Highlight tab characters"), columnspan=2)
        self.add_checkbox(
            "view.highlight_current_line",
            tr("Highlight current line (requires reopening the editor)"),
            columnspan=2,
        )

        self.add_checkbox(
            "edit.automatic_calltips",
            tr("Automatically show parameter info after typing '('"),
            columnspan=2,
            pady=(group_spacing, 0),
        )
        self.add_checkbox(
            "edit.automatic_completions",
            tr("Automatically propose completions while typing"),
            columnspan=2,
        )
        self.add_checkbox(
            "edit.automatic_completion_details",
            tr("Automatically show documentation for completions"),
            columnspan=2,
        )
        self.add_checkbox(
            "edit.tab_request_completions_in_editors",
            tr("Request completions with Tab-key in editors"),
            columnspan=2,
        )
        self.add_checkbox(
            "edit.tab_request_completions_in_shell",
            tr("Request completions with Tab-key in Shell"),
            columnspan=2,
        )

        self.add_checkbox(
            "view.show_line_numbers", tr("Show line numbers"), pady=(group_spacing, 0), columnspan=2
        )
        self.add_checkbox(
            f"file.make_saved_shebang_scripts_executable",
            tr("Make saved shebang scripts executable"),
            columnspan=2,
        )

        self._line_length_var = get_workbench().get_variable("view.recommended_line_length")
        label = ttk.Label(
            self,
            text=tr("Line length guide (use 0 to turn off)"),
        )
        label.grid(row=20, column=0, sticky=tk.W, pady=(group_spacing, 0))
        self._line_length_combo = ttk.Combobox(
            self,
            width=4,
            exportselection=False,
            textvariable=self._line_length_var,
            state="readonly",
            values=[0, 60, 70, 80, 88, 90, 100, 110, 120],
        )
        self._line_length_combo.grid(
            row=20, column=1, sticky=tk.W, padx=10, pady=(group_spacing, 0)
        )

        self._tab_width_var = get_workbench().get_variable("edit.tab_width")
        label = ttk.Label(self, text=tr("Maximum width of a tab character"))
        label.grid(
            row=31,
            column=0,
            sticky=tk.W,
        )
        self._tab_width_combo = ttk.Combobox(
            self,
            width=4,
            exportselection=False,
            textvariable=self._tab_width_var,
            state="readonly",
            values=[1, 2, 3, 4, 5, 6, 7, 8],
        )
        self._tab_width_combo.grid(
            row=31,
            column=1,
            sticky=tk.W,
            padx=10,
        )

        self._indent_width_var = get_workbench().get_variable("edit.indent_width")
        label = ttk.Label(self, text=tr("Indent width"))
        label.grid(
            row=32,
            column=0,
            sticky=tk.W,
        )
        self._indent_width_combo = ttk.Combobox(
            self,
            width=4,
            exportselection=False,
            textvariable=self._indent_width_var,
            state="readonly",
            values=[1, 2, 3, 4, 5, 6, 7, 8],
        )
        self._indent_width_combo.grid(
            row=32,
            column=1,
            sticky=tk.W,
            padx=10,
        )

        self.add_checkbox(
            "edit.indent_with_tabs",
            tr("Indent with tab characters (not recommended for Python)"),
            columnspan=2,
            pady=(group_spacing, 0),
        )

        self.columnconfigure(1, weight=1)

    def apply(self):
        ConfigurationPage.apply(self)
        get_workbench().get_editor_notebook().update_appearance()
        shell = get_shell(create=False)
        if shell is not None:
            shell.update_appearance()


def load_plugin() -> None:
    get_workbench().add_configuration_page("editor", tr("Editor"), EditorConfigurationPage, 30)
