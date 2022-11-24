from app import app
import app.db as db
from unittest.mock import ANY
import app.models as models
from flask_testing import TestCase
import copy

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

class BaseTestCase(TestCase):
	def setUp(self):
		super().setUp()
		
		models.Base.metadata.drop_all(db.engine)
		models.Base.metadata.create_all(db.engine)
		
		self.user_1_data = {
			"username": "unittestuser1",
			"password": "unittestuserpassword1"
		}
			
		self.user_1_data_hashed = {
			"username": self.user_1_data["username"],
			"password": bcrypt.generate_password_hash(self.user_1_data["password"]).decode('utf-8')
		}
			
		self.user_2_data = {
			"username": "unittestuser2",
			"password": "unittestuserpassword2"
		}
			
		self.user_2_data_hashed = {
			"username": self.user_2_data["username"],
			"password": bcrypt.generate_password_hash(self.user_2_data["password"]).decode('utf-8')
		}		
			
		user1 = models.User(username=self.user_1_data_hashed['username'], password=self.user_1_data_hashed['password'])
		user2 = models.User(username=self.user_2_data_hashed['username'], password=self.user_2_data_hashed['password'])
		db.session.add(user1)
		db.session.add(user2)
		db.session.commit()
		
		self.user2_id = user2.id
		
		self.user_1_private_playlist = {
			"name": "unittestprivateplaylist",
			"is_public": False,
			"owner_id": user1.id
		}
		
		self.user_2_public_playlist = {
			"name": "Sunittestpublicplaylist",
			"is_public": True,
			"owner_id": user2.id
		}
		
		playlist1 = models.Playlist(name=self.user_1_private_playlist['name'], is_public=self.user_1_private_playlist['is_public'], owner_id=self.user_1_private_playlist['owner_id'])
		playlist2 = models.Playlist(name=self.user_2_public_playlist['name'], is_public=self.user_2_public_playlist['is_public'], owner_id=self.user_2_public_playlist['owner_id'])
		db.session.add(playlist1)
		db.session.add(playlist2)
		db.session.commit()
		
		self.playlist1_id = playlist1.id
		self.playlist2_id = playlist2.id
		
		self.track1 = {
			"title": "track1",
			"playlist_id": playlist1.id,
			"youtube_id": "DK6IRG4CAbw"
		}
		
		self.track2 = {
			"title": "track2",
			"playlist_id": playlist2.id,
			"youtube_id": "DK6IRG4CAbz"
		}
		
		tracksInPlaylist1 = models.TracksInPlaylist(title=self.track1["title"], playlist_id=self.track1["playlist_id"],youtube_id=self.track1["youtube_id"])
		tracksInPlaylist2 = models.TracksInPlaylist(title=self.track2["title"], playlist_id=self.track2["playlist_id"],youtube_id=self.track2["youtube_id"])
		db.session.add(tracksInPlaylist1)
		db.session.add(tracksInPlaylist2)
		db.session.commit()
		
		self.track1_id = tracksInPlaylist1.youtube_id
		self.track2_id = tracksInPlaylist2.youtube_id
			
			
	def tearDown(self):
		db.session.rollback()
		
	def create_app(self):
		return app
	
	def get_auth_header(self, credentials):
		resp = self.client.post('user/login',json=credentials)
		access_token = resp.json['token']
		return {"Authorization": f'Bearer {access_token}'}
		
class Testlogin(BaseTestCase):
	def test_user_login(self):
		resp = self.client.post('user/login',json=self.user_1_data)
		
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.json, {'token': ANY})
		
		resp = self.client.post('user/login',json={"wrong": "wrong"})
		
		self.assertEqual(resp.status_code, 400)
		
		test_user = copy.deepcopy(self.user_1_data)
		test_user["username"] = "notexistingunittestusername"
		resp = self.client.post('user/login',json=test_user)
		
		self.assertEqual(resp.status_code, 404)
		
		test_user = copy.deepcopy(self.user_1_data)
		test_user["password"] = "notexistingunittestpassword"
		resp = self.client.post('user/login',json=test_user)
		
		self.assertEqual(resp.status_code, 400)
		

	
class TestGetUser(BaseTestCase):
	def test_get_user(self):
		resp = self.client.get('user/', headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 200)
		
		resp = self.client.get(f'user/{999999}', headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 404)

		
class TestdeleteUser(BaseTestCase):
	def test_delete_user(self):
	
		test_token = self.get_auth_header(self.user_1_data)
		resp = self.client.delete('user/', headers=self.get_auth_header(self.user_1_data))
		
		self.assertEqual(resp.status_code, 200)
		
		resp = self.client.delete('user/', headers=test_token)
		
		self.assertEqual(resp.status_code, 404)
		
class TestLogoutUser(BaseTestCase):
	def test_logout_user(self):
		resp = self.client.post('user/logout', headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 200)
		
class TestpostUser(BaseTestCase):
	def test_post_user(self):
		resp = self.client.post('user/', json={"wrong":"wrong"})
		
		self.assertEqual(resp.status_code, 400)
		
		resp = self.client.post('user/', json=self.user_1_data)
		
		self.assertEqual(resp.status_code, 400)
		
		testuser = self.user_1_data
		testuser["username"] = "unittestuser3"
		resp = self.client.post('user/', json=testuser)
		
		self.assertEqual(resp.status_code, 201)
		
class TestPutUser(BaseTestCase):
	def test_put_user(self):
		
		test_token = self.get_auth_header(self.user_2_data)
		
		resp = self.client.put('user/', json={"wrong":"wrong"}, headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 400)
		
		test_user = copy.deepcopy(self.user_2_data)
		test_user["password"] = "wrong password"
		resp = self.client.put('user/', json=test_user, headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 400)
		
		test_user = copy.deepcopy(self.user_2_data)
		test_user["username"] = self.user_1_data["username"]
		resp = self.client.put('user/', json=test_user, headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 400)
		
		test_user = copy.deepcopy(self.user_2_data)
		test_user["new_password"] = "new_password"
		resp = self.client.put('user/', json=test_user, headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 200)
		
		self.client.delete('user/', headers=test_token)
		resp = self.client.put('user/', json=self.user_2_data, headers=test_token)
				
		self.assertEqual(resp.status_code, 404)
		
class TestGetTrack(BaseTestCase):
	def test_get_track(self):
		resp = self.client.get(f'tracks/{self.track1_id}/',)
		
		self.assertEqual(resp.status_code, 200)
		
		resp = self.client.get(f'tracks/{-4}/',)
		
		self.assertEqual(resp.status_code, 404)

"""		
class TestGetSearch(BaseTestCase):
	def test_search_track(self):
		resp = self.client.get(f'search/tracks/?id={self.track1_id}')
		
		self.assertEqual(resp.json, [
			{ "title": self.track1["title"],
			"video_id": self.track1["youtube_id"]
			},
			{"title": self.track2["title"],
			"video_id": self.track2["youtube_id"]
			}
		])
"""

class TestGetPlaylist(BaseTestCase):
	def test_get_playlists(self):
		resp = self.client.get('playlists/')
		
		self.assertEqual(resp.json, [
			{
			"id": self.playlist2_id,
			"is_public": self.user_2_public_playlist["is_public"],
			"name": self.user_2_public_playlist["name"],
			"owner_id": self.user_2_public_playlist["owner_id"],
			"tracks": [
			{"title": self.track2["title"], "youtube_id": self.track2["youtube_id"]}
			]
			}
		])
		
class TestCreatePlaylist(BaseTestCase):
	def test_create_playlist(self):
	
		test_token = self.get_auth_header(self.user_2_data)
		
		resp = self.client.post('playlists/', json={"wrong": "wrong"}, headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 400)
		
		resp = self.client.post('playlists/', json={"name": self.user_2_public_playlist["name"], "is_public": self.user_2_public_playlist["is_public"]}, headers=test_token)
		
		self.assertEqual(resp.status_code, 201)
		
		self.client.delete('user/', headers=test_token)
		resp = self.client.post('playlists/', json={"name": self.user_2_public_playlist["name"], "is_public": self.user_2_public_playlist["is_public"]}, headers=test_token)
		
		self.assertEqual(resp.status_code, 404)
		
class TestGetPlaylistById(BaseTestCase):
	def test_get_playlist_by_id(self):
		
		resp = self.client.get(f'playlists/{999999}/', json={"wrong": "wrong"}, headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 404)
		
		resp = self.client.get(f'playlists/{self.playlist1_id}/')
		
		self.assertEqual(resp.status_code, 401)
		
		resp = self.client.get(f'playlists/{self.playlist1_id}/', headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 403)
		
		resp = self.client.get(f'playlists/{self.playlist1_id}/', headers=self.get_auth_header(self.user_1_data))
		
		self.assertEqual(resp.status_code, 200)
		
		
		
		
class TestPutPlaylists(BaseTestCase):
	def test_put_playlists(self):
		
		resp = self.client.put(f'playlists/{self.user2_id}/', json={"wrong": "wrong"}, headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 400)
		
		resp = self.client.put(f'playlists/{999999}/', json={"name": self.user_2_public_playlist["name"], "is_public": self.user_2_public_playlist["is_public"] }, headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 404)
		
		resp = self.client.put(f'playlists/{self.playlist1_id}/', json={"name": self.user_2_public_playlist["name"], "is_public": self.user_2_public_playlist["is_public"] }, headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 403)
		
		resp = self.client.put(f'playlists/{self.playlist2_id}/', json={"name": self.user_2_public_playlist["name"], "is_public": self.user_2_public_playlist["is_public"] }, headers=self.get_auth_header(self.user_2_data))
		
		self.assertEqual(resp.status_code, 200)
		
class TestDeletePLaylists(BaseTestCase):
	def test_delete_playlists(self):
		
		resp = self.client.delete(f'playlists/{999999}/', headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 404)
		
		resp = self.client.delete(f'playlists/{self.playlist1_id}/', headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 403)
		
		resp = self.client.delete(f'playlists/{self.playlist2_id}/', headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 200)
		
class TestAddTrackToPlaylist(BaseTestCase):
	def test_add_track_to_playlist(self):
	
		resp = self.client.post(f'playlists/{self.playlist2_id}/tracks/',json={"wrong":"wrong"} , headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 400)
		
		resp = self.client.post(f'playlists/{999999}/tracks/',json={"youtube_id": "_E3FGh4b04s"} , headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 404)
		
		resp = self.client.post(f'playlists/{self.playlist1_id}/tracks/',json={"youtube_id": "_E3FGh4b04s"} , headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 403)
		
		resp = self.client.post(f'playlists/{self.playlist2_id}/tracks/',json={"youtube_id": self.track2_id} , headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 400)
		
		resp = self.client.post(f'playlists/{self.playlist2_id}/tracks/',json={"youtube_id": "0123456789y"} , headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 404)
		
		resp = self.client.post(f'playlists/{self.playlist2_id}/tracks/',json={"youtube_id": "qrZnLpJx_zY"} , headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 201)
		
class TestDeleteTrackFromPlaylist(BaseTestCase):
	def test_delete_track_from_playlist(self):
		
		resp = self.client.delete(f'playlists/{999999}/tracks/{self.track2_id}/', headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 404)
		
		resp = self.client.delete(f'playlists/{self.playlist1_id}/tracks/{self.track2_id}/', headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 403)
		
		resp = self.client.delete(f'playlists/{self.playlist2_id}/tracks/{self.track1_id}/', headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 404)
		
		resp = self.client.delete(f'playlists/{self.playlist2_id}/tracks/{self.track2_id}/', headers=self.get_auth_header(self.user_2_data))

		self.assertEqual(resp.status_code, 200)
		
class TestSearchTracks(BaseTestCase):
	def test_search_tracks(self):
		
		resp = self.client.get('/search/tracks/?query=track1')
		
		self.assertEqual(resp.status_code, 200)
		
class TestSearchUsers(BaseTestCase):
	def test_search_users(self):
		
		resp = self.client.get(f'/search/users/?query=unittestuser2')
		
		self.assertEqual(resp.status_code, 200)
		
class TestSearchPLaylists(BaseTestCase):
	def test_search_playlists(self):
		
		resp = self.client.get(f'/search/playlists/?query=unittestpublicplaylist')
		
		self.assertEqual(resp.status_code, 200)
		

		
		
	


	
	 
			
		
	
