import os, json
import requests
import streamlit as st

class WatsonxAI:

    '''
    GRANITE_3B_CODE_INSTRUCT = "ibm/granite-3b-code-instruct"
    GRANITE_8B_CODE_INSTRUCT = "ibm/granite-8b-code-instruct"
    GRANITE_20B_CODE_INSTRUCT = "ibm/granite-20b-code-instruct"
    GRANITE_34B_CODE_INSTRUCT = "ibm/granite-34b-code-instruct"
    GRANITE_13B_CHAT_V2 = "ibm/granite-13b-chat-v2"
    GRANITE_13B_INSTRUCT_V2 = "ibm/granite-13b-instruct-v2"
    GRANITE_3_8B_INSTRUCT = "ibm/granite-3-8b-instruct"
    SLATE_30M_ENGLISH_RTRVR = "ibm/slate-30m-english-rtrvr"
    SLATE_30M_ENGLISH_RTRVR_V2 = "ibm/slate-30m-english-rtrvr-v2"
    SLATE_125M_ENGLISH_RTRVR = "ibm/slate-125m-english-rtrvr"
    SLATE_125M_ENGLISH_RTRVR_V2 = "ibm/slate-125m-english-rtrvr-v2"

    GRANITE_20B_MULTILINGUAL = "ibm/granite-20b-multilingual"
    LLAMA_3_70B_INSTRUCT = "meta-llama/llama-3-70b-instruct"
    LLAMA_3_3_70B_INSTRUCT = "meta-llama/llama-3-3-70b-instruct"
    LLAMA_3_2_11B_VISION_INSTRUCT = "meta-llama/llama-3-2-11b-vision-instruct"
    LLAMA_3_2_90B_VISION_INSTRUCT = "meta-llama/llama-3-2-90b-vision-instruct"

    MS_MARCO_MINILM_L_12_V2 = "cross-encoder/ms-marco-minilm-l-12-v2"
    ALL_MINILM_L6_V2 = "sentence-transformers/all-minilm-l6-v2"
    ALL_MINILM_L12_V2 = "sentence-transformers/all-minilm-l12-v2"
    MULTILINGUAL_E5_LARGE = "intfloat/multilingual-e5-large"

    OLLAMA_GRANITE_8B_CODE_INSTRUCT = "granite3-dense:8b"
    OLLAMA_GRANITE_3_1_8B_CODE_INSTRUCT = "granite3.1-dense:8b"
    OLLAMA_GRANITE_2B_CODE_INSTRUCT = "granite3-dense:2b"
    '''

    OLLAMA_GRANITE_3_1_8B_CODE_INSTRUCT = "granite3.1-dense:8b"
    
    def watsonx_gen_stream(self,prompt,model_id,max_output=4000,temp=0,top_k=1,repeat_penalty=1.1,stream=True):

        url = "http://127.0.0.1:11434/api/generate"
        params = {
            "temperature": 0.1,
            "repeat_penalty":1.1,
            "top_p":1,
            "top_k":50,
            "num_predict":max_output,
            "stop":["[/INST]","<|user|>","<|endoftext|>","<|assistant|>","<eof>"]
        }

        body = {
            "model":model_id,
            "options":params,
            "stream":stream,
            "prompt":prompt
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            # "Authorization": f"Bearer {self.access_token}" # No need for authorization as it is locally hosted using Ollama
        }

        response = requests.post(
            url,
            headers=headers,
            json=body,
            stream=True
        )


        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        yield ""
        # Stream the response
        for line in response.iter_lines():
            if line:  # Ensure the line is not empty
                decoded_line = line.decode("utf-8").strip()
                
                # Check if the line starts with "data: "
                if decoded_line.startswith("data: "):
                    json_data = decoded_line[len("data: "):]  # Remove the "data: " prefix
                else:
                    json_data = decoded_line
                try:
                    # Attempt to load the JSON data
                    data = json.loads(json_data)
                    print("Check Data:",data)
                    generated_text = data.get("response", "")

                    yield generated_text
                    if data.get("done"):
                        st.session_state['tokens']['prompt_tokens'] = data.get("prompt_eval_count")
                        st.session_state['tokens']['response_tokens'] = data.get("eval_count")
                        st.session_state['tokens']['total_tokens'] = data.get("prompt_eval_count") + data.get("eval_count")
                        print("Checking session state tokens",st.session_state['tokens'])

                except json.JSONDecodeError:
                    print("Failed to decode JSON:", json_data)
                except Exception as e:
                    print("An error occurred:", e)

        yield ""