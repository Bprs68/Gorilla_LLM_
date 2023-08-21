import openai
import re
import streamlit as st


openai.api_key = "YOUR_OPENAI_API_KEY"
openai.api_base = "http://zanino.millennium.berkeley.edu:8000/v1"

st.set_page_config(layout="wide")

def get_gorilla_response(prompt, model):
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Sorry, something went wrong: {e}"

def extract_code_from_output(output):
    code_marker = "<<<code>>>:"
    code_start = output.find(code_marker) + len(code_marker)
    code = output[code_start:]
    return code.strip()

def extract_code_from_output_as_newlines(output):
    code_marker = "<<<code>>>:"
    code_start = output.find(code_marker) + len(code_marker)
    code = output[code_start:]
        
    code_lines = re.split(r'\\n', code)  # Split using escaped newline characters
    code_lines = [line.replace("\\\\", "\\") for line in code_lines]  # Handle escaped backslashes
    code_lines = code_lines[:-1]
    return code_lines

def main():
    st.title("Gorilla LLM Demo App🦍")
    st.write("It is not a conversational chatbot like ChatGPT.")
    st.write("It is specifically for getting codes and access to APIs of a large number of models in HuggingFace, TensorFlow and TorchHub.")

    input_prompt = st.text_area("Enter your prompt below:", placeholder="I want to generate image from text.....")
    selected_model = st.selectbox("Select a model:", ["gorilla-7b-hf-v1", "gorilla-7b-th-v0", "gorilla-mpt-7b-hf-v0"])

    if st.button("Gorilla Magic"):
        with st.spinner("Generating code..."):
            if len(input_prompt) > 0:
                
                if selected_model in ["gorilla-7b-th-v0", "gorilla-mpt-7b-hf-v0"]:
                    result = get_gorilla_response(prompt=input_prompt, model=selected_model)
                    result_lines = re.split(r'\\n', result)
                    result_lines = [line.replace("\\\\", "\\") for line in result_lines][:-1]
                    for line in result_lines:
                        st.write(line)


                    code_lines = extract_code_from_output_as_newlines(result)
                    if code_lines:
                        for line in code_lines:
                            st.code(line, language='python')
                    else:
                        st.warning("No code snippet extracted.")

                elif selected_model == "gorilla-7b-hf-v1":
                    result = get_gorilla_response(prompt=input_prompt, model=selected_model)
                    domain = result[result.find("<<<domain>>"):result.find("<<<api_call>>>")]
                    st.write(domain)
                    api_call= result[result.find("<<<api_call>>"):result.find("<<<api_provider>>>")]
                    st.write(api_call)
                    api_provider = result[result.find("<<<api_provider>>"):result.find("<<<explanation>>")]
                    st.write(api_provider)
                    explanation = result[result.find("<<<explanation>>"):result.find("<<<code>>>")]
                    st.write(explanation)

                    code = extract_code_from_output(result)
                    if code:
                        st.code(code, language='python')
                    else:
                        st.warning("No code snippet extracted.")                    

            else:
                st.warning("Please enter a prompt.")
  

if __name__ == "__main__":
    main()
