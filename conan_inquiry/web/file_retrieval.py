import hashlib
import os

import re
from datetime import datetime

from jsmin import jsmin


class WebFiles:
    replacement_html_re = re.compile(r'<import +href="([^"]+)"(/>|></import>)')
    replacement_js_re = re.compile(r'//import (\S+)')
    dir = os.path.join(os.path.dirname(__file__), 'files')
    # FIXME: Add  'packages.js', 'packages.json', to list after package upadates are working to deploy them
    files_generated = ['wishlist.json', 'wishlist.js']

    # Returns full path to a file
    def full_name(self, name):
        if self.is_constant(name):
            return os.path.join(os.path.dirname(__file__), '..', '..', 'build', name)
        return os.path.join(self.dir, name)

    # Check if file exists
    def exists(self, name):
        return os.path.exists(self.full_name(name))

    def minimize_content(self, input, format):
        result = ''
        if format == 'js':
            result = jsmin(input)

        return result

    # Returns content of a file, minimized and adjusted
    def adjust_content(self, name: str, content, debug=False):
        content = self.replacement_html_re.sub(lambda x: self.get_file(self.full_name(x.group(1))), content)
        content = self.replacement_js_re.sub(lambda x: self.get_file(self.full_name(x.group(1))), content)
        if not debug:
            content = content.replace('CACHE_BUSTER',
                                    hashlib.md5(datetime.now().isoformat().encode('utf-8')).hexdigest())

        if name.endswith('.js'):
            content = self.minimize_content(content, 'js')

        return content

    # Returns content of a file, minimized and adjusted
    def get_file(self, name: str, debug=False):
        with open(name, 'r', encoding="utf8") as f:
            result = f.read()
            result = self.adjust_content(name, result, debug)

        return result

    # Returns file size
    def size(self, name):
        return os.path.getsize(self.full_name(name))

    # Returns list of file names which are important for web deployment
    def deploy_names(self):
        files = self.files_generated
        for entry in os.listdir(self.dir):
            if os.path.isfile(os.path.join(self.dir, entry)) and not entry.startswith('_'):
                files.append(entry)
        return files

    # required?
    def full_names(self):
        files = []
        for file_gen in self.files_generated:
            if os.path.isfile(self.full_name(file_gen)):
                files.append(self.full_name(file_gen))
        for entry in os.listdir(self.dir):
            if os.path.isfile(self.full_name(entry)) and not entry.startswith('_'):
                files.append(self.full_name(entry))
        return files

    def is_constant(self, name):
        if name in self.files_generated:
            return True
        return False
