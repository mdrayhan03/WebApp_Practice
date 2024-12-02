import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import id_token
from google.auth.transport.requests import Request
import webbrowser, requests, http.server, socketserver, threading, json, sys
sys.stdout.reconfigure(encoding='utf-8')

class Gmail_login :
    def __init__(self) :
        pass

    def authenticate_with_google(self):
        # Path to your client_secret.json file from Google Cloud Console
        base_dir = os.path.dirname(os.path.abspath(__file__))
        CLIENT_SECRET_FILE = os.path.join(base_dir, 'client_secret.json')

        # Specify the required scopes
        SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]

        # Run the OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)

        # Get the ID token from the credentials
        id_token_jwt = credentials.id_token

        print("ID Token:", id_token_jwt)

        # Verify the token
        return self.verify_google_token(id_token_jwt)


    def verify_google_token(self, token):
        try:
            # Replace YOUR_GOOGLE_CLIENT_ID with your actual client ID
            CLIENT_ID = "640195498777-rrl6ivvoq8g1qm1ijkgj4ueoffvg2o9o.apps.googleusercontent.com"
            idinfo = id_token.verify_oauth2_token(token, Request(), CLIENT_ID)

            # Extract user information
            # print("User ID:", idinfo["sub"])
            # print("Email:", idinfo["email"])
            # print("Name:", idinfo["name"])
            # print("Picture:", idinfo["picture"])
            # print(type(idinfo))
            return idinfo

        except ValueError as e:
            print("Invalid token:", e)
            return None

# Define the HTTP server handler
class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, facebook_login_instance=None, **kwargs):
        self.facebook_login_instance = facebook_login_instance
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if "/callback" in self.path:
            query = self.path.split("?")[1]
            params = dict(x.split("=") for x in query.split("&"))
            self.facebook_login_instance.auth_code = params.get("code")  # Save the auth code
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Login successful! You can close this window.")

class Facebook_login:
    def __init__(self):
        self.APP_ID = "823545683091187"
        self.APP_SECRET = "ff42adf4e792e42d2ec7bd60b864d86a"
        self.REDIRECT_URI = "http://localhost:5000/callback"
        self.auth_code = None

    def start_server(self):
        # Pass the Facebook_login instance to the handler
        handler = lambda *args, **kwargs: CallbackHandler(*args, facebook_login_instance=self, **kwargs)
        with socketserver.TCPServer(("localhost", 5000), handler) as httpd:
            httpd.handle_request()

    def work(self):
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()

        # Open the Facebook login URL in the browser
        print("Opening Facebook login page...")
        fb_login_url = (
            f"https://www.facebook.com/v16.0/dialog/oauth?"
            f"client_id={self.APP_ID}&redirect_uri={self.REDIRECT_URI}&scope=email,public_profile"
        )
        webbrowser.open(fb_login_url)

        # Wait until the auth_code is captured
        while self.auth_code is None:
            pass  # Busy wait until the auth code is set

        # Exchange the authorization code for an access token
        token_url = (
            f"https://graph.facebook.com/v16.0/oauth/access_token?"
            f"client_id={self.APP_ID}&redirect_uri={self.REDIRECT_URI}&client_secret={self.APP_SECRET}&code={self.auth_code}"
        )
        token_response = requests.get(token_url).json()
        access_token = token_response.get("access_token")

        # Use the access token to fetch user information
        user_info_url = "https://graph.facebook.com/me?fields=id,name,email&access_token=" + access_token
        user_info = requests.get(user_info_url).json()

        # Display user info
        info = json.dumps(user_info, ensure_ascii=False, indent=4)
        info = json.loads(info)

        print(info)

        return info