import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
tool = hasattr(os, 'environ')  # dummy reference to utilize dotenv
load_dotenv()

API_URL = os.getenv('API_URL', 'http://localhost:8000')

# Use Streamlit's built-in rerun function

st.title('API Key Health Monitor')

tab1, tab2 = st.tabs(['Manage Keys', 'Health Logs'])

with tab1:
    st.header('Registered API Keys')
    try:
        keys = requests.get(f'{API_URL}/keys').json()
    except Exception as e:
        st.error(f'Error connecting to API: {e}')
        st.stop()

    for key in keys:
        st.subheader(f"{key['service']} - {key['name']} (ID: {key['id']})")
        st.write(f"Last Checked: {key.get('last_checked', 'N/A')}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Check now {key['id']}", key=f"check_{key['id']}"):
                res = requests.post(f'{API_URL}/keys/{key['id']}/checks/trigger')
                if res.ok:
                    st.success('Health check triggered')
                else:
                    st.error(f'Error: {res.text}')
                st.rerun()
        with col2:
            if st.button(f"Delete {key['id']}", key=f"del_{key['id']}"):
                res = requests.delete(f'{API_URL}/keys/{key['id']}')
                if res.ok:
                    st.success('Key deleted')
                else:
                    st.error(f'Error: {res.text}')
                st.rerun()

    st.info('Ready to add a new API key? Follow these steps:')
    with st.expander('➕ Add New API Key', expanded=True):
        with st.form('add_key'):
            SERVICE_OPTIONS = ['OpenAI', 'Azure OpenAI', 'Google Gemini', 'Ollama', 'Custom']
            service = st.selectbox('Service', SERVICE_OPTIONS, help='Select which platform you want to monitor')
            name = st.text_input(
                'Name', placeholder='e.g. Production OpenAI Key',
                help='Give your key a friendly name to identify it in the dashboard'
            )
            key_value = st.text_input(
                'Key Value', type='password', placeholder='sk-...',
                help='Enter the secret token or key exactly as provided by the service'
            )
            metadata = {}
            # Add contextual descriptions and options per service
            if service == 'OpenAI':
                st.markdown('**OpenAI Test:** GET `/v1/models` will be performed. [API Docs](https://platform.openai.com/docs/models)')
                DEFAULT_MODELS = [
                    'gpt-4', 'gpt-4o', 'gpt-4o-mini',
                    'gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'text-davinci-003'
                ]
                # Option to fetch live model list
                fetch_live = st.checkbox(
                    'Fetch live model list',
                    help='Use your API key to fetch current models from OpenAI'
                )
                models = DEFAULT_MODELS
                if fetch_live:
                    try:
                        headers = {"Authorization": f"Bearer {key_value}"}
                        resp = requests.get(
                            "https://api.openai.com/v1/models",
                            headers=headers, timeout=10.0
                        )
                        data = resp.json().get('data', [])
                        models = [m['id'] for m in data]
                        st.success(f"Fetched {len(models)} models")
                    except Exception as e:
                        st.error(f"Error fetching models: {e}")
                model = st.selectbox(
                    'OpenAI Model', models,
                    help='Select which model to test'
                )
                metadata = {'model': model}
            elif service == 'Azure OpenAI':
                st.markdown('**Azure OpenAI Test:** Using your AZURE variables from `.env`, select the deployment to check.')
                AZURE_MODELS = ['gpt-4o', 'o3-mini']
                deployment = st.selectbox(
                    'Azure Deployment', AZURE_MODELS,
                    help='The deployment name you configured in Azure OpenAI'
                )
                metadata = {'deployment': deployment}
            elif service == 'Google Gemini':
                st.markdown('**Google Gemini Test:** Checks a lightweight call to the embedding or chat endpoint.')
                gm_opts = [
                    os.getenv('GEMINI_2_5_PRO_MODEL', 'gemini-2.5-pro-exp-03-25'),
                    os.getenv('GEMINI_EMBEDDING_MODEL', 'gemini-embedding-exp')
                ]
                gemini_model = st.selectbox(
                    'Gemini Model', gm_opts,
                    help='Select the Gemini model variant (chat or embeddings)'
                )
                metadata = {'model': gemini_model}
            elif service == 'Ollama':
                st.markdown('**Ollama Test:** Pings your local Ollama server to list models.')
                host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
                st.text_input('Ollama Host', host, disabled=True)
                metadata = {'host': host}
            elif service == 'Custom':
                st.markdown('**Custom API Test:** Define your own HTTP health-check.')
                with st.expander('⚙️ Custom API Configuration', expanded=False):
                    json_template = {
                        "url": "https://api.example.com/health",
                        "method": "GET",
                        "headers": {"Authorization": "Bearer {key}"},
                        "body": None,
                        "success_status_codes": [200]
                    }
                    metadata_input = st.text_area(
                        'Custom Configuration (JSON)',
                        value=json.dumps(json_template, indent=2), height=200,
                        help='Edit this JSON: URL, method, headers, body, success_status_codes'
                    )
                    try:
                        metadata = json.loads(metadata_input)
                    except json.JSONDecodeError as e:
                        st.error(f'Invalid JSON: {e}')
                        metadata = {}
            submitted = st.form_submit_button('Add Key')
            if submitted:
                payload = {'service': service, 'name': name, 'key_value': key_value}
                if metadata:
                    payload['metadata'] = metadata
                res = requests.post(f'{API_URL}/keys', json=payload)
                if res.ok:
                    st.success('Key added successfully')
                else:
                    st.error(f'Error: {res.text}')
                st.rerun()

with tab2:
    st.header('Health Check Logs')
    key_id = st.number_input('API Key ID', min_value=1, step=1)
    if st.button('Load Logs'):
        res = requests.get(f'{API_URL}/keys/{key_id}/checks')
        if res.ok:
            logs = res.json()
            st.dataframe(logs)
        else:
            st.error(f'Error: {res.text}')
