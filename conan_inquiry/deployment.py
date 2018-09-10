from datetime import datetime
from tempfile import TemporaryDirectory

import os
import subprocess
import hashlib

from conan_inquiry.web.file_retrieval import WebFiles


def deploy():
    dir = os.path.join(os.path.dirname(__file__), "../gh-pages")
    print('* Deploying with dir:', dir)

    def git(subcmd, *args, **kwargs):
        kwargs.setdefault('cwd', os.path.join(dir, 'conan_inquiry'))

        print('* Running: git', subcmd)
        retcode = subprocess.call(['git', subcmd] + list(args), **kwargs)
        if retcode != 0:
            raise ChildProcessError('Unable to run the command')

    repository = os.getenv('GITHUB_REPO', 'https://{}@github.com/Croydon/conan_inquiry'.format(os.getenv('GITHUB_TOKEN')))

    if not os.path.exists(dir):
        os.makedirs(dir)
        git('clone', repository, '--branch', 'gh-pages', '--single-branch', cwd=dir)
    else:
        git('pull')

    files = WebFiles()

    for file in files.names():
        with open(os.path.join(dir, 'conan_inquiry', file), 'wt') as f:
            f.write(files.get_file(file, debug=False))
        git('add', os.path.join(dir, 'conan_inquiry', file))

    git('commit', '-am', 'Automatic deployment')
    git('push')
    print('* Deployment successful!')
