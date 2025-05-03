import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import os
import json

def login_user():
    if "user_info" in st.session_state:
        return st.session_state["user_info"]

    client_secrets_file = os.path.join("client_secrets.json")  # path to your Google credentials

    # Load client secrets (Google API credentials)
    with open(client_secrets_file) as f:
        client_secrets = json.load(f)

    client_id = client_secrets["web"]["client_id"]
    client_secret = client_secrets["web"]["client_secret"]
    redirect_uri = "https://autism-spectrum-disorder--medical-analyisis.streamlit.app/"  # update if deployed

    # Set up OAuth 2.0 session
    oauth = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)
    authorization_url, state = oauth.authorization_url('https://accounts.google.com/o/oauth2/v2/auth', scope=["openid", "email", "profile"])

    # Display the login link
    st.sidebar.markdown(f"[Login with Google]({authorization_url})")

    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        oauth.fetch_token(
            'https://oauth2.googleapis.com/token',
            authorization_response=st.experimental_get_query_params().get('url', [])[0],
            client_secret=client_secret
        )
        # Fetch user info
        user_info = oauth.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
        st.session_state["user_info"] = {"name": user_info["name"], "email": user_info["email"]}
        return st.session_state["user_info"]

    return None
