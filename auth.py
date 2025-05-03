import streamlit as st
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import os
import json

def login_user():
    if "user_info" in st.session_state:
        return st.session_state["user_info"]

    client_secrets_file = os.path.join("client_secrets.json")  # path to your Google credentials

    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["openid", "email", "profile"],
        redirect_uri="http://localhost:8501"  # update this if deployed
    )

    auth_url, _ = flow.authorization_url(prompt='consent')
    st.sidebar.markdown("[Login with Google](%s)" % auth_url)

    query_params = st.query_params
    if "code" in query_params:
        flow.fetch_token(code=query_params["code"])
        credentials = flow.credentials
        request = google.auth.transport.requests.Request()
        id_info = id_token.verify_oauth2_token(credentials.id_token, request, flow.client_config["client_id"])
        user_info = {"name": id_info["name"], "email": id_info["email"]}
        st.session_state["user_info"] = user_info
        return user_info

    return None
