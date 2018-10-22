import os
import subprocess
from shutil import copy

from conan_inquiry.web.file_retrieval import WebFiles


def deploy():
    dir = os.path.join(os.path.dirname(__file__), "../gh-pages")
    print('* Deploying with dir:', dir)

    def git(subcmd, *args, **kwargs):
        kwargs.setdefault('cwd', os.path.join(dir, 'conan_inquiry'))

        print('* Running: git', subcmd)
        retcode = subprocess.call(['git', subcmd] + list(args), **kwargs)

        # Something went wrong, commit is allowed to fail in this context as we might have nothing new to commit
        if retcode != 0 and subcmd != "commit":
            raise ChildProcessError('Unable to run the command')

    repository = os.getenv('GITHUB_REPO', 'https://{}@github.com/Croydon/conan_inquiry'.format(os.getenv('GITHUB_TOKEN')))

    if not os.path.exists(dir):
        os.makedirs(dir)
        git('clone', repository, '--branch', 'gh-pages', '--single-branch', cwd=dir)
    else:
        git('pull')

    if not os.path.exists('build'):
        os.makedirs('build')

    for file in os.listdir(os.path.join(os.path.dirname(__file__), 'web', 'files')):
        copy(os.path.join(os.path.dirname(__file__), 'web', 'files', file), 'build')

    files = WebFiles()

    for file in files.deploy_names():
        file_path = os.path.join(os.path.dirname(__file__), '..', 'build', file)

        if not file_path.endswith('.png'):
            with open(file_path, 'r+', encoding="utf8") as f:
                data = files.adjust_content(file, f.read(), debug=False)
                f.seek(0)
                f.write(data)
                f.truncate()
        copy(file_path, os.path.join('gh-pages', 'conan_inquiry'))

    git('add', '-A')
    git('commit', '-am', 'Automatic deployment')
    git('push')
    print('* Deployment successful!')
