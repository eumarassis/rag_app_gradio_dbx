# Add favicon as an HTML element with JavaScript
head_html = """
<script>
    var link = document.createElement('link');
    link.rel = 'icon';
    link.href = 'https://www.databricks.com/en-website-assets/favicon-32x32.png';  // Path to your favicon
    document.head.appendChild(link);

    // Create the script element for Marked.js
    const markedScript = document.createElement('script');
    markedScript.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
    markedScript.type = 'text/javascript';

    // Append the script to the document head
    document.head.appendChild(markedScript);
</script>

<script>

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    modal = document.getElementById('myModal');
    if (event.target == modal) {
      modal.style.display = 'none';
    }
  }
  
  function openModal() {
    document.getElementById('myModal').style.display = 'block';
    document.getElementById('myModalContent').innerHTML = marked.parse(document.getElementById('references-section-div-hidden').innerHTML);
  }
</script>
"""

auto_scroll_js = """
    function Scrolldown() {
        let targetNode = document.querySelector('[aria-label="chatbot conversation"]');
        // Options for the observer (which mutations to observe)
        let config = { attributes: true, childList: true, subtree: true };

        // Callback function to execute when mutations are observed
        let callback = (mutationList, observer) => {
            targetNode.scrollTop = targetNode.scrollHeight;
            let position = targetNode.innerText.indexOf('<input id="references-section-div-hidden"');
            
        };

        // Create an observer instance linked to the callback function
        let observer = new MutationObserver(callback);

        // Start observing the target node for configured mutations
        observer.observe(targetNode, config);
    }
"""

# Custom CSS to style the chat input and response
# Define custom CSS to style the input and chat response
css = """

textarea {
    border: 3px solid lightgray !important;    /* Strong (thicker) dark border */
    padding: 10px !important;             /* Optional: Add some padding inside the textarea */
    border-radius: 5px !important ;        /* Optional: Slightly rounded corners */
    font-size: 16px !important;           /* Optional: Adjust font size */
    color: #fff !important;               /* Optional: Text color */
    box-sizing: border-box;    /* Ensure padding doesn't affect the width */
    height: 50px !important;    /* Set the height of the textarea */
}

#chatbot {
    background-color: lightgray !important;
    border: 1px !important;
    line-height: 2.9 !important; 
}
/* Hide the "Use via API" message */
#colab-button { display: none !important; }

/* Hide the "Built with Gradio" logo */
footer { display: none !important; }

/* Style the clear button with a border */
button#clear-btn {
    background-color: white !important;
    color: black !important;
    border: 2px solid black !important;

    cursor: pointer;
}

#header-logo {
    display: flex; 
    align-items: center; 
    cursor: hard;
}

#header-logo .logo-img {
    background-color: white !important;
    width: 50px; 
    height: 50px; 
    margin-right: 10px;
    border-radius: 8px;
}

#header-logo h1 {
    margin-top: -5px;
}

#header-logo a {
    text-decoration: none; 
    color: inherit;
}

#header-message {
  font-size: 18px;
  line-height: 2.3;
}

#references-container {
    margin-top: -20px;
    display: flex;
    align-items: center;
    gap: 8px; /* Adjust spacing between title and links as needed */
}

#references-section-title {
    font-weight: bold;
    cursor: pointer;
}

#sup-links {
    font-size: smaller;
    white-space: nowrap; /* Prevent line breaks in the sup links */
}

#sup-links a {

    text-decoration: none;
    margin-right: 10px; /* Space between sup numbers */
}

#sup-links a:hover {
    text-decoration: underline; /* Optional hover effect */
}
"""



# Custom HTML and CSS for the modal
modal_html = """
<div id="myModal" class="modal">
  <div class="modal-content">
    <span class="close" id="myModalClose" onclick="document.getElementById('myModal').style.display='none';">&times;</span>
    <div id="myModalContent"></div>
  </div>
</div>
<style>
/* Modal styles */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 50%; /* Center horizontally */
  top: 50%; /* Center vertically */
  transform: translate(-50%, -50%); /* Move by half the width and height to fully center */
  width: 80%; /* 50% of the screen width */
  height: 80%; /* 50% of the screen height */
  background-color: var(--background-fill-primary); 

}

/* Modal Content */
.modal-content {

  margin: auto;
  padding: 20px;
  border: 1px solid #888;
  color: black; /* White text */
  border-radius: 10px; /* Slight rounding of corners */
  width: 100%; /* 50% of the screen width */
  height: 100%; /* 50% of the screen height */
  overflow-y: auto; /* Enable vertical scrolling */
  line-height: 2.4; 
}

/* The Close Button */
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: #fff;
  text-decoration: none;
  cursor: pointer;
}
</style>

"""