import os
import tempfile
import unittest

from app.main import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass


    def test_upload_file(self):
        with tempfile.NamedTemporaryFile(suffix=".ipynb") as tmp:
            # Write some content to file
            tmp.write(b"Dummy file")
            tmp.seek(0)

            # Send request with dummy data
            rv = self.app.post('/refactor', data={'file': (tmp, 'test.ipynb')})
            assert b'refactored_test.ipynb' in rv.data


    def test_download_file(self):
        # Send request to download non-existent file
        rv = self.app.get('/download/non_existent_file.ipynb')
        assert rv.status_code == 404

        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False) as tmp:
            tmp.write(b"Dummy refactored file")
        filename = os.path.basename(tmp.name)

        # Place file in downloads folder
        download_folder = app.config['DOWNLOAD_FOLDER']
        os.makedirs(download_folder, exist_ok=True)
        os.replace(tmp.name, os.path.join(download_folder, "refactored_" + filename))

        # Send request to download file
        rv = self.app.get('/download/' + filename)
        assert rv.status_code == 200
        assert rv.headers['Content-Disposition'] == f'attachment; filename="refactored_{filename}"'


if __name__ == '__main__':
    unittest.main()