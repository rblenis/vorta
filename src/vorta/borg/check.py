from .borg_thread import BorgThread


class BorgCheckThread(BorgThread):

    def started_event(self):
        self.app.backup_started_event.emit()
        self.app.backup_progress_event.emit(self.tr('Starting consistency check...'))

    def finished_event(self, result):
        self.app.backup_finished_event.emit(result)
        self.result.emit(result)
        self.app.backup_progress_event.emit(self.tr('Check completed.'))

    @classmethod
    def prepare(cls, profile):
        ret = super().prepare(profile)
        if not ret['ok']:
            return ret

        ret['cmd'] = [
            'borg', 'check', '--info', '--log-json',
            f'{profile.repo.url}']
        ret['ok'] = True

        return ret
