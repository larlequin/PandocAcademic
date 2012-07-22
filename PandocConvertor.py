# A Sublime Text plugin to convert a Pandoc document into multiple formats:
#   - html
#   - docx
#   - pdf
#   - beamer
#
# The plug-in also deal with options embedded in the file to add more functions
#  such as a table of content, a bibliography or enumerate sections.
#
# Different bibliography styles and templates could be chosen.
#
# G.T. Vallet -- Lyon2 University
# 2012/06/24  -- GPLv3
# 2012/07/10  -- v02 -- Always launch associated application and better syntax
# 2012/07/20  -- v02.5 -- Fix the bug when pictures are included, convert PDF
#                           doesn't run. Need to change the path of the figures.
#
# Inspired and cannibalized from Pandoc Renderer plugin
#  https://github.com/jclement/SublimePandoc

import sublime, sublime_plugin
import subprocess
import webbrowser
import tempfile
import time
import sys
import os
import re

class PandocConvertorCommand(sublime_plugin.TextCommand):
    """ Convert a Pandoc file to HTML or Docx fileformat
        Options allow to add a table of contents, a bibliography,
          or to enumerate the sections.
    """
    def is_visible(self):
        return True


    def is_enabled(self):
        if self.view.score_selector(0, "text.pandoc") > 0 or \
            self.view.score_selector(0, "text.html.markdown") > 0 or \
            self.view.score_selector(0, "text.html.markdown.multimarkdown") > 0:
            return True


    def getTemplatePath(self, filename):
        path = os.path.join(sublime.packages_path(),'Pandoc Academic','Styles',filename)
        if not os.path.isfile(path):
            raise Exception(filename + " file not found!")

        return path


    def grabContent(self):
        """ A simple function to grab the content of the current buffer
        """
        region = sublime.Region(0, self.view.size())

        return self.view.substr(region).encode('utf8')


    def template(self, cmd, target, contents):
        """ A function to select the appropriate template
        """
        regex_docstyle = re.compile(r'\[\[DOCSTYLE=(\w+)\]\]')
        if regex_docstyle.search(contents) != None:
            style = regex_docstyle.search(contents).groups()[0]
            if target == 'html':
                cmd.append('--template='+self.getTemplatePath(style+".html"))
            elif target == 'docx':
                cmd.append('--reference-docx='\
                       +self.getTemplatePath(style+".docx"))
            elif target == 'beamer':
                cmd.append('-V')
                cmd.append('theme:'+style)
        else:
            if target == 'html':
              cmd.append('--template='+self.getTemplatePath("template.html"))
            elif target == 'docx':
                cmd.append('--reference-docx='\
                        +self.getTemplatePath("reference.docx"))

        return cmd


    def opt(self, cmd, target, dir_path):
        """ A function to search for options embedded in the Pandoc file
              adding table of contents, bibliography and/or section number
        """
        # Grab the content of the current buffer
        contents = self.grabContent()

        # Check if a custom path is provided
        regex_path = re.compile(r'\[\[PATH=(.+)\]\]')
        if regex_path.search(contents) != None:
            pandoc_path = regex_path.search(contents).groups()[0]
            cmd[0] = pandoc_path
        # Options embedded in the documents to turn on features in the output.
        if '[[TOC]]' in contents:
            cmd.append("--toc")
        if '[[NUM]]' in contents:
            cmd.append("-N")
        if '[[BIB]]' in contents:
            cmd.append("--bibliography")
            cmd.append(os.path.splitext(self.view.file_name())[0]+".bib")
            # Style options
            regex_bibstyle = re.compile(r'\[\[BIBSTYLE=(\w+)\]\]')
            if regex_bibstyle.search(contents) != None:
                bibstyle = regex_bibstyle.search(contents).groups()[0]
                cmd.append("--csl")
                cmd.append(self.getTemplatePath(bibstyle+".csl"))
        if '[[HEADER]]' in contents:
            cmd.append("--include-in-header="+os.path.split(self.view.file_name())[0]+"/header")
        if '[[NORENDER]]' in contents:
            openAfter = False
        else:
            # By default, launch the associated program of the file
            openAfter=True

        # Check for templates and styles options
        cmd = self.template(cmd, target, contents)

        # Adapt the path of the figures included (if any)
        re_img = "!\[.*\]\((.+)\)"  # Regex to find the figures
        for match in re.finditer(re_img, contents):
            contents = contents.replace(match.group(1), os.path.join(dir_path, match.group(1)))

        return cmd, openAfter, contents


    def buildCommand(self, target):
        """ A function to build the final Pandoc command to run
            Take the target and return the command and the output file
        """
        # Extract the filename
        file_name   = self.view.file_name().encode(sys.getfilesystemencoding())
        filepath = os.path.splitext(file_name)[0]
        dir_path = os.path.split(file_name)[0]
        if not self.view.file_name(): raise Exception("Buffer must be saved!")
        if target == 'beamer':
            output_file = filepath + ".pdf"
        else:
            output_file = filepath + "." + target

        # Adding separated blocks of text to run the command in sublime text
        cmd = ['pandoc', '--smart', '--standalone']
        # Check for options in the Pandoc file
        cmd, openAfter, contents = self.opt(cmd, target, dir_path)

        # Create a temporary file to handle the contents
        tmp_md = tempfile.NamedTemporaryFile(delete=False, suffix=".md")
        tmp_md.write(contents)
        tmp_md.close()

        # Complete the command function
        if target != 'pdf':
            cmd.append('-t')
            cmd.append(target)
        cmd.append(tmp_md.name)
        cmd.append("-o")
        cmd.append(output_file)


        return cmd, output_file, openAfter


    def status(self, filename):
        """ Update the status monitor of sublime text
        """
        self.view.set_status('pandoc','File converted to ' + filename)
        print "File converted to:", filename
        time.sleep(2)
        self.view.erase_status('pandoc')


    def run(self, edit, target="html"):
        # Call the build command function to construct the final pandoc command
        cmd, output_filename, openAfter = self.buildCommand(target)
        # Run the main command to convert the file
        try:
            subprocess.call(cmd)
        except Exception as e:
            sublime.error_message("Unable to execute Pandoc.\
                                    \n\nDetails: {0}".format(e))

        # Update the status
        self.status(output_filename)
        # View the converted file in the browser if openAfter true
        if openAfter:
            webbrowser.open(output_filename)