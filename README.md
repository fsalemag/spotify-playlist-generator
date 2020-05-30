# Spotify playlist generator
Generates a playlist with random tracks based on your listening pattern of the previous 4 weeks

### Usage
1. Clone repository
2. Create folder configs with 1 file: configs.yaml
3. Run main.py

### Configs file structure
```
auth:
  client_id: <client-id>
  client_secret : <client-secret>
  redirect_uri: <redirect-url>
  scope: >
    ugc-image-upload
    user-read-playback-state
    user-modify-playback-state
    user-read-currently-playing
    streaming
    app-remote-control
    user-read-email
    user-read-private
    playlist-read-collaborative
    playlist-modify-public
    playlist-read-private
    playlist-modify-private
    user-library-modify
    user-library-read
    user-top-read
    user-read-playback-position
    user-read-recently-played
    user-follow-read
    user-follow-modify 
```
To get the client id and secret you must create an application in https://developer.spotify.com/dashboard/applications, and from the dashboards you can get both fields.

You must then add the <redirect-url> of you choice to the allowed urls in the "edit settings" tab. You can choose whatever url you want, it is not relevant.

Under scope there are all the possible permissions available at the time of writting, you can select whichever permissions you want, or keep them all as is.



