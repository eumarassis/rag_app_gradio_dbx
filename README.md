# RAG Gradio app using Databricks Model Serving

This repo delivers a RAG app using Gradio, MLflow Tracing, and Databricks Mosaic AI to build a quick chat interface for testing and rapid customer feedback with support for streaming and citations from a vector database. It extends the app built on the Databricks Demo [“Build High-Quality RAG Apps with Mosaic AI Agent Framework and Agent Evaluation, Model Serving, and Vector Search.”](https://www.databricks.com/resources/demos/tutorials/data-science-and-ai/lakehouse-ai-deploy-your-llm-chatbot?itm_data=demo_center)


Gradio is a convenient framework to demo machine learning models with a friendly web interface. Gradio is not a replacement for a fully-fledged chat experience built on robust UX frameworks like React or native app development. However, it is a great tool for early demonstration and to prove the functionality of the model vs. focusing on building a pixel-perfect interface from the beginning.

Customizing Gradio can be tricky, but basic CSS and HTML5 skills are all you need. In this demo, I wanted to show a modal popup to render the citation based on content retrieved from the Vector Database, Databricks Vector Search. So, all we needed was a mix of Python code to render HTML content and CSS.
