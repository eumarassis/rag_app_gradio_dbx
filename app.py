import gradio as gr
import os
from gradio.themes.utils import sizes
from typing import List, Tuple, Generator, Optional

from dbx_endpoint_util import parse_chunk, extract_databricks_output, call_model_stream, generate_reference_section
from ui_const import head_html, auto_scroll_js, css, modal_html

endpoint_name = os.getenv('DATABRICKS_ENDPOINT_NAME', 'default_endpoint_url_here')
token = os.getenv('DATABRICKS_API_TOKEN', 'default_token_here')


def respond(message: str, history: List[Tuple[str, str]]) -> Generator[Tuple[List[Tuple[str, str]], str], None, None]:
    """
    Handles the user input and streams the response, updating chat history.
    
    Args:
        message (str): The user's input message.
        history (List[Tuple[str, str]]): The chat history containing user and assistant messages.
    
    Yields:
        Tuple[List[Tuple[str, str]], str]: Updated chat history and input reset signal.
    """
    if len(message.strip()) == 0:
        yield history, "ERROR: The question should not be empty"  # Return error if the message is empty

    try:
        messages = []  # Initialize messages list
        if history:
            for human, assistant in history:
                messages.append({"content": human, "role": "user"})  # Add user messages to messages list
                messages.append({"content": assistant, "role": "assistant"})  # Add assistant messages to messages list

        messages.append({"content": message, "role": "user"})  # Add the latest user message
        history.append((message, ""))  # Append the new message to history

        response_stream = call_model_stream(messages=messages, endpoint_name=endpoint_name, token=token)  # Call the model to get streaming response
        accumulated_response = ""
        accumulated_content = ""

        for chunk in response_stream:
            accumulated_response += chunk  # Append the chunk to the accumulated response
            content = parse_chunk(chunk)  # Parse the chunk for content
            if content:
                accumulated_content += content  # Append content to accumulated content
                history[-1] = (message, accumulated_content)  # Update chat history
                yield history, ""  # Yield updated chat history and reset the input box

    except Exception as error:
        yield history, f"ERROR: Requesting endpoint {endpoint_name}: {error}"  # Handle exception

    # Generate reference section
    json_databricks_response = extract_databricks_output(accumulated_response)
    references_text, urls = generate_reference_section(json_databricks_response)
    references_section_html = ""
                        
    if len(references_text) > 150:  # Only append references if they are longer than a chunk
        sup_links = ''.join([f'<sup><a href="{url}" target="_blank">{i + 1}</a></sup>' for i, url in enumerate(urls)])

        references_section_html = f"""
            <div style="display:none" id="references-section-div-hidden">{references_text}</div>
            <p id="references-container">
                <span id="references-section-title" onclick="openModal();" title="View Reference Sources">VIEW SOURCES</span>
                <span id="sup-links">{sup_links}</span>
            </p>
            """
        
   # Render the response with markdown and append the references section as escaped HTML
    history[-1] = (message, accumulated_content + references_section_html)
    yield history, ""


# Define your theme
theme = gr.themes.Soft(
    text_size=sizes.text_md,
    radius_size=sizes.radius_lg,
    spacing_size=sizes.spacing_lg,
)

# Create a Gradio app using Blocks
with gr.Blocks(head=head_html,theme=theme, css=css, js=auto_scroll_js, title="RAG Sample App: Gradio + Databricks") as demo:

    # Title and description
    gr.Markdown(f"""
    <div id="header-logo">
        <a href="">
            <img src="https://www.gradio.app/_app/immutable/assets/gradio.CHB5adID.svg" alt="Logo" class="logo-img" >
        </a>            
        <h1 >RAG Sample App: Gradio with Databricks</a>  </h1>        
    </div>
    """)
   
    gr.Markdown("""<div id="header-message">This is a sample RAG application built with Gradio, connected to a Databricks Serving Endpoint using Model Gateway. It demonstrates how to display citations based on Databricks Mosaic AI Vector Search.</div>""")
    
    # Chatbot and Textbox
    chatbot = gr.Chatbot(elem_id="chatbot", show_copy_button=True, bubble_full_width=True, show_label=False, render_markdown=True, sanitize_html=False)

    
    with gr.Row():
        txt_input = gr.Textbox(
            placeholder="Message the Chatbot", 
            elem_id="input-box", 
            show_label=False, 
            scale=7
        )
        submit_btn = gr.Button("Submit", elem_id="submit-btn", size="sm", variant="secondary")

 
    # Define the interaction
    submit_btn.click(respond, inputs=[txt_input, chatbot], outputs=[chatbot, txt_input])
    txt_input.submit(respond, inputs=[txt_input, chatbot], outputs=[chatbot, txt_input])
   
    
    # Example questions (interactive)
    examples = gr.Examples(
        examples=[
            ["Unity Catalog: What is a Shared Cluster?"],
            ["Delta Sharing: How to revoke a share?"],
            ["AI/BI: Benefits of using Genie"],
        ],
        
        inputs=txt_input
    )
    

    with gr.Row():
        clear_btn = gr.Button("Clear Chat", size="sm", variant="secondary")
        
    clear_btn.click(lambda: None, None, chatbot, queue=False)  # Clear the chatbox        
    
    gr.HTML(modal_html )    

# Queue management
demo.queue(default_concurrency_limit=100)

#auth_user = ("user", "d@tabricks")

auth_user  = None 

demo.launch(auth_message="Welcome to RAG Sample App - Gradio with Databricks.", auth=auth_user)

# Mount the Gradio app
#app = gr.mount_gradio_app(app, demo, path="/", )
