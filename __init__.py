import os
import pytest

caldav_args = {
    # Those credentials are configured through the Travis UI
    'username': os.environ['DAVICAL_USERNAME'].strip(),
    'password': os.environ['DAVICAL_PASSWORD'].strip(),
    'url': 'https://brutus.lostpackets.de/davical/caldav.php/',
    'verify': False,
    'verify_fingerprint': \
        '36:B0:8B:AD:66:C6:FB:B0:1B:4E:CC:8A:07:C8:FF:37:49:AD:87:DE'
}


def _clear_collection(s):
    for href, etag in s.list():
        s.delete(href, etag)


class ServerMixin(object):
    @pytest.fixture
    def davical_args(self):
        if self.storage_class.fileext == '.ics':
            return caldav_args
        elif self.storage_class.fileext == '.vcf':
            pytest.skip('No carddav')
        else:
            raise RuntimeError()

    @pytest.fixture
    def get_storage_args(self, davical_args, request):
        def inner(collection='test'):
            args = davical_args
            if collection is not None:
                assert collection.startswith('test')
                args = self.storage_class.create_collection(collection, **args)
                s = self.storage_class(**args)
                _clear_collection(s)
                assert not list(s.list())
            return args
        return inner
