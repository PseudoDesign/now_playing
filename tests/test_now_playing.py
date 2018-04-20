from unittest import TestCase
from unittest.mock import patch, MagicMock, call
from now_playing import keys
from now_playing import lastfm


class TestLastFm(TestCase):
    @patch('pylast.LastFMNetwork')
    def test_connect_uses_pylast_and_last_fm(self, last_fm_network):
        api = "api_key"
        secret = "secret_key"
        last_fm_network.return_value = "network"
        return_value = lastfm.connect(api, secret)
        last_fm_network.assert_called_once_with(api_key=api, api_secret=secret)
        self.assertEqual(return_value, "network")

    def test_current_track(self):
        network = MagicMock()
        user = MagicMock()
        track = MagicMock()
        network.get_user.return_value = user
        user.get_now_playing.return_value = track
        username = "test"
        return_value = lastfm.current_track(network, username)
        network.get_user.assert_called_once_with(username)
        user.get_now_playing.assert_called_once()
        self.assertEqual(return_value, track)


class TestLastFmSaveTrackInfo(TestCase):

    def setUp(self):
        self.location = "test_location"
        self.track = MagicMock()
        self.track_title = "track"
        self.artist = "artist"
        self.album = MagicMock()
        self.album_title = "album"
        self.album_image_url = "pseudo.design/img.png"

        self.track.artist = self.artist
        self.track.title = self.track_title
        self.track.get_album.return_value = self.album
        self.album.title = self.album_title
        self.album.get_cover_image.return_value = self.album_image_url

    @patch('now_playing.lastfm.save_image')
    @patch('now_playing.lastfm.save_text')
    def test_save_track_info(self, save_text, save_image):

        lastfm.save_track_info(self.track, self.location)

        save_text_calls = [
            call(self.track_title, self.location, "title.txt"),
            call(self.artist, self.location, "artist.txt"),
            call(self.album_title, self.location, "album.txt")
        ]

        save_text.assert_has_calls(save_text_calls)
        save_image.assert_called_with(self.album_image_url, self.location, "album_art.png")


class TestKeys(TestCase):
    def test_api_key_is_string(self):
        self.assertEqual(type(keys.API_KEY), str)

    def test_secret_key_is_string(self):
        self.assertEqual(type(keys.SECRET_KEY), str)
