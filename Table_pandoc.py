# A script to create a pandoc grid table from the current selection
# Cells must be separated by 2 or more spaces
# Empty cells should be indicated by NA
#
# GT Vallet -- Lyon 2 University
# 2012/07/26 -- v01

import re
import sublime
import sublime_plugin

class PandocTableCommand(sublime_plugin.TextCommand):

    def is_enabled(self):
        if self.view.score_selector(0, "text.pandoc") > 0 or \
            self.view.score_selector(0, "text.html.markdown") > 0 or \
            self.view.score_selector(0, "text.html.markdown.multimarkdown") > 0:
            return True

    def run(self, edit):
        # Grab the content of the current selection and split it by lines
        sel = self.view.sel()[0]
        raw_txt = self.view.substr(sel)
        # Format raw_txt into usable data
        txt = self.format_txt(raw_txt)
        # Find the number of columns
        nb_col = len(txt[0])
        # Length max by column
        col_widths = self.width_col(nb_col, txt)
        # Build the final table and replace the current selection
        table = self.final_table(txt, col_widths)
        self.view.replace(edit, sel, table)
        print "Table formatted"


    def format_txt(self, txt):
        # Remove previous table structure markers (---, ===, +, |)
        txt = re.sub("-{3,}|={3,}|\+|\|", "", txt)
        # Split text by lines
        txt = txt.split('\n')
        # Split lines by cells and create a list of lists of cells
        new_txt = []
        for line in txt:
            if line != "":
                line = re.sub("\s+$", "", line)
                line_split = re.compile('\t|\s{2,}').split(line)
                new_line = []
                for cell in line_split:
                    new_line.append(re.sub("^\s+", "", cell))
                new_txt.append(new_line)
        return new_txt


    def width_col(self, nb_col, txt):
        """ Determine the maximum possible width for each column
            Add 2 to these widths to handle space between cell content
        """
        col_len = []
        for col in range(nb_col):
            cur_col_len = 0
            for line in txt:
                if len(line[col]) > cur_col_len:
                    cur_col_len = len(line[col])
            col_len.append(cur_col_len)
        return map(lambda x: x + 2, col_len)


    def create_lines(self, header, widths):
        """ Function developed in the nvie-vim-rst-table plugin
            Create header lines and regular lines based on the columns widths
        """
        if header:
            linechar = '='
        else:
            linechar = '-'
        sep = '+'
        parts = []
        for width in widths:
            parts.append(linechar * width)
        if parts:
            parts = [''] + parts + ['']
        return sep.join(parts)


    def build_row(self, line, widths):
        """ For each cell of a row, add column separators and space to remain
            space of cell (up to the maximum width of the column)
            Empty cells --NA-- are replace by empty spaces
        """
        to_print = []
        for idx, item in enumerate(line):
            if item == "NA":
                item = ""
            space = widths[idx]-len(item)-1
            to_print.append('| ' + item + " " * space)
        return "".join(to_print)


    def final_table(self, txt, col_widths):
        """ Create the final grid table
            Add regular and header lines and column separators
        """
        new_table = []
        for idx, line in enumerate(txt):
            if idx == 1:
                new_table.append(self.create_lines(True, col_widths))
                new_table.append(self.build_row(line, col_widths) + "|")
            else:
                new_table.append(self.create_lines(False, col_widths))
                new_table.append(self.build_row(line, col_widths) + "|")
        new_table.append(self.create_lines(False, col_widths))
        return "\n".join(new_table)