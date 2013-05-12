import os

import git

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VENDOR_PATH = os.path.join(ROOT, 'integration/vendor')
VENDOR = 'https://github.com/puppetlabs/marionette-collective.git'


class IntegrationTestCaseMixin(object):
    def get_vendor_ref(self, rev):
        if not os.path.exists(VENDOR_PATH):
            repo = git.Repo.clone_from(VENDOR, VENDOR_PATH)
        else:
            repo = git.Repo(VENDOR_PATH)

        try:
            reference = repo.rev_parse(rev)
        except git.BadObject:
            # Let's try remote branch, probably origin
            remote = repo.remote()
            for ref in remote.refs:
                if ref.name == '{name}/{rev}'.format(name=remote.name,
                                                     rev=rev):
                    remote_ref = ref
                    break
            else:
                raise git.Badobject(rev)
            new_branch = repo.create_head(rev)
            new_branch.set_tracking_branch(remote_ref)
            reference = new_branch
        repo.head.reference = reference
        repo.head.reset(index=True, working_tree=True)
        return repo
