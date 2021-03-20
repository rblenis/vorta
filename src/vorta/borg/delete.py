from .borg_thread import BorgThread


class BorgDeleteThread(BorgThread):

    def started_event(self):
        self.app.backup_started_event.emit()
        self.app.backup_progress_event.emit(self.tr('Deleting archive...'))

    def finished_event(self, result):
        self.app.backup_finished_event.emit(result)
        self.result.emit(result)
        self.app.backup_progress_event.emit(self.tr('Archive deleted.'))

    @classmethod
    def prepare(cls, profile):
        ret = super().prepare(profile)
        if not ret['ok']:
            return ret

        ret['cmd'] = [
            'borg', 'delete', '--info', '--log-json',
            f'{profile.repo.url}']
        ret['ok'] = True

        return ret
