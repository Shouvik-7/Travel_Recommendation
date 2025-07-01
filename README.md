uv 
Bash CMDs 
1. uv init
2. uv venv 
3. .venv\Scripts\activate
4. uv add -r requirements.txt


Alternate 
Bash 

1. python -m venv .venv
2. .venv\Scripts\activate
3. pip install -r requirements.txt



```Bash
aws configure
```

```Bash
set OPENAI_API_KEY=your-api-key-here
```


Run rag.ipynb to train the vectorstore and see recommendation results



For Streamlit app

```Bash 
streamlit run app.py
```


Copy glue_script to AWS Glue python Script for Loading data from S3 to Glue Data Catalog