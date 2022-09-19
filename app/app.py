import streamlit as st

from pollination_streamlit.selectors import (get_api_client, job_selector)

api_client = get_api_client()

job = job_selector(api_client)

def handleSelectArtifact():
    bytes = st.session_state['sel_artifact'].download().read()
    st.session_state['text'] = bytes.decode('utf8')

def formatArtifact(artifact):
    if 'key' in artifact.__dict__:
        return artifact.key
    else:
        return ''

if 'text' not in st.session_state:
    st.session_state['text'] = ''

if 'artifacts' not in st.session_state:
    st.session_state['artifacts'] = []

def followArtifactTree(artifact_array):
    for artifact in artifact_array:
        if artifact.is_folder:
            followArtifactTree(artifact.list_children())
        else :
              st.session_state['artifacts'].append(artifact)
    
if job is not None:
    artifacts = job.list_artifacts()

    if artifacts is not None:
        followArtifactTree(artifacts)

st.selectbox(
  'Select an artifact', 
  options= st.session_state['artifacts'], 
  key='sel_artifact', 
  on_change=handleSelectArtifact, 
  format_func=formatArtifact
)

st.download_button(
    label='Download Text File', 
    data=st.session_state['text'], 
    file_name=st.session_state['sel_artifact'].key if st.session_state['sel_artifact'] is not None else '', 
    key='download-button',
    disabled=st.session_state['text'] == ''
  )