import os
import pytest
import uuid
import requests

caldav_args = {
    # Those credentials are configured through the Travis UI
    'username': os.environ['DAVICAL_USERNAME'].strip(),
    'password': os.environ['DAVICAL_PASSWORD'].strip(),
    'url': 'https://brutus.lostpackets.de/davical/caldav.php/',
    'verify': False,
    'verify_fingerprint': \
        '36:B0:8B:AD:66:C6:FB:B0:1B:4E:CC:8A:07:C8:FF:37:49:AD:87:DE'
}


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
            assert collection and collection.startswith('test')

            for _ in range(4):
                collection += uuid.uuid4()
                args = self.storage_class.create_collection(collection, **args)
                s = self.storage_class(**args)
                if not list(s.list()):
                    request.addfinalizer(
                        lambda: s.session.request('DELETE', ''))
                    return args

            raise RuntimeError('Failed to find free collection.')
        return inner
