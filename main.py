import requests
import yaml
import os
import json
from pprint import pprint
import random

class Spotify(object):
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.configs = self._load_configs()

        self.auth_url = "https://accounts.spotify.com/{}"
        self.api_endpoint = "https://api.spotify.com/v1/{}"

        self.token = self._generate_token()

        self.user_info = self._get_user_info()

    def _load_configs(self):
        with open(os.path.join(self.base_dir, "configs", "configs.yaml"), 'r') as fid:
            return yaml.safe_load(fid)

    def _generate_token(self):
        auth = self.configs["auth"]

        # If there is already a token in place
        if os.path.isfile(os.path.join(self.base_dir, "configs", "token.json")):
            return self._refresh_token()

        # Generate a new token
        else:
            print("Must log in to generate token, access following url:")

            response = requests.get(
                self.auth_url.format("authorize"),
                params={
                    "client_id": auth["client_id"],
                    "response_type": "code",
                    "redirect_uri": auth["redirect_uri"],
                    "scope": "ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing streaming app-remote-control user-read-email user-read-private playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private user-library-modify user-library-read user-top-read user-read-playback-position user-read-recently-played user-follow-read user-follow-modify"
                }
            )

            print(response.url)
            code = input("After log in, paste the resulting url (from the browser) here:\n").split("code=")[1]

            # Request actual token
            response = requests.post(
                self.auth_url.format("api/token"),
                data={
                    "client_id": auth["client_id"],
                    "client_secret": auth["client_secret"],
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": auth["redirect_uri"],
                }
            ).json()

            with open(os.path.join(self.base_dir, "configs", "token.json"), "w") as fid:
                json.dump(response, fid, indent=4)

        return response["access_token"]

    def _refresh_token(self):
        auth = self.configs["auth"]
        with open(os.path.join(self.base_dir, "configs", "token.json")) as fid:
            token = json.load(fid)

        response = requests.post(
            self.auth_url.format("api/token"),
            data={
                "grant_type": "refresh_token",
                "refresh_token": token["refresh_token"],
                "client_id": auth["client_id"],
                "client_secret": auth["client_secret"],
            }
        ).json()

        return response["access_token"]

    # User
    def _get_user_info(self):
        return requests.get(
            self.api_endpoint.format("me"),
            headers={"Authorization": f"Bearer {self.token}"}
        ).json()

    # Playlists 
    def get_user_playlists(self):
        return requests.get(
            self.api_endpoint.format("me/playlists"),
            headers={"Authorization": f"Bearer {self.token}"}
        ).json().get("items")

    def create_playlist(self, name):
        id = self.user_info["id"]

        return requests.post(
            self.api_endpoint.format(f"users/{id}/playlists"),
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            },
            json={
                "name": name
            }
        ).json()       

    def update_playlist(self, playlist_name):
        # Check if playlist exists
        user_playlists = self.get_user_playlists()
        playlist = list(filter(lambda playlist: playlist['name'] == playlist_name, user_playlists))

        if not playlist:
            playlist = self.create_playlist(playlist_name)
        else:
            playlist = playlist.pop()

        return requests.put(
            self.api_endpoint.format(f"playlists/{playlist['id']}/tracks"),
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            },
            json={
                "uris": [track["uri"] for track in self.get_recommendations()]
            }
        ).json()

    # Affinity
    def get_top_tracks(self):
        return requests.get(
            self.api_endpoint.format("me/top/tracks"),
            headers={
                "Authorization": f"Bearer {self.token}",
            },
            params={
                "limit": 20,
                "time_range": "short_term"
            }
        ).json()["items"]

    def get_recommendations(self):
        top_tracks_ids = [track["id"] for track in self.get_top_tracks()]

        return requests.get(
            self.api_endpoint.format("recommendations"),
            headers={
                "Authorization": f"Bearer {self.token}"
            },
            params={
                "limit": 20,
                "seed_tracks": ",".join(random.sample(top_tracks_ids, k=5))
            }
        ).json()["tracks"]


if __name__ == "__main__":
    sp = Spotify()
    sp.update_playlist("Auto generated")
