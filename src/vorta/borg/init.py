from vorta.models import RepoModel
from .borg_thread import BorgThread, FakeProfile, FakeRepo


class BorgInitThread(BorgThread):

    def started_event(self):
        self.updated.emit(self.tr('Setting up new repo...'))

    @classmethod
    def prepare(cls, params):

        # Build fake profile because we don't have it in the DB yet.
        profile = FakeProfile(
            FakeRepo(params['repo_url'], 999, params['extra_borg_arguments'],
                     params['encryption']), 'Init Repo', params['ssh_key']
        )

        ret = super().prepare(profile)
        if not ret['ok']:
            return ret

        ret['ok'] = False  # Set back to false, so we can do our own checks here.

        ret['cmd'] = [
            "borg", "init", "--info", "--log-json",
            f"--encryption={params['encryption']}",
            params['repo_url']]

        ret['additional_env'] = {
            'BORG_RSH': 'ssh -oStrictHostKeyChecking=no'
        }

        ret['encryption'] = params['encryption']
        ret['password'] = params['password']
        ret['ok'] = True

        return ret

    def process_result(self, result):
        if result['returncode'] == 0:
            new_repo, _created = RepoModel.get_or_create(
                url=result['params']['repo_url'],
                defaults={
                    'encryption': result['params']['encryption'],
                    'extra_borg_arguments': result['params']['extra_borg_arguments'],
                }
            )
            if new_repo.encryption != 'none':
                self.keyring.set_password("vorta-repo", new_repo.url, result['params']['password'])
            new_repo.save()
