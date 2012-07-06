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
#
# Inspired and cannibalized from Pandoc Renderer plugin
#  https://github.com/jclement/SublimePandoc
import sublime, sublime_plugin
import subprocess
import webbrowser
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
       return self.view.score_selector(0, "source.pandoc") > 0


    def getTemplatePath(self, filename):
        path = os.path.join(sublime.packages_path(),'Pandoc','Styles',filename)
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


    def opt(self, cmd, target):
        """ A function to search for options embedded in the Pandoc file
              adding table of contents, bibliography and/or section number
        """
        # Grab the content of the current buffer
        contents = self.grabContent()

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

        # Check for templates and styles options
        cmd = self.template(cmd, target, contents)

        return cmd


    def buildCommand(self, target):
        """ A function to build the final Pandoc command to run
            Take the target and return the command and the output file
        """
        # Extract the filename
        file_name   = self.view.file_name()
        if not self.view.file_name(): raise Exception("Buffer must be saved!")
        if target == 'beamer':
            output_file = os.path.splitext(self.view.file_name())[0] + ".pdf"
        else:
            output_file = os.path.splitext(self.view.file_name())[0] + "." + target

        # Adding separated blocks of text to run the command in sublime text
        cmd = ['pandoc']
        if target != 'pdf':
            cmd.append('-t')
            cmd.append(target)
        cmd.append('--standalone')
        cmd.append('--smart')
        cmd.append(file_name)
        cmd.append("-o")
        cmd.append(output_file)
        # Check for options in the Pandoc file
        cmd = self.opt(cmd, target)

        return cmd, output_file


    def status(self, filename):
        """ Update the status monitor of sublime text
        """
        self.view.set_status('pandoc','File converted to ' + filename)
        print "File converted to:", filename
        time.sleep(2)
        self.view.erase_status('pandoc')


    def run(self, edit, target="html", openAfter=True):
        # Call the build command function to construct the final pandoc command
        cmd, output_filename = self.buildCommand(target)
        # Run the main command to convert the file
        try:
            subprocess.call(cmd)
        except Exception as e:
            sublime.error_message("Unable to execute Pandoc.\
                                    \n\nDetails: {0}".format(e))
        # Update the status
        self.status(output_filename)
        # View the converted file in the browser if openAfter true
        if openAfter and target == "html":
            webbrowser.open(output_filename)