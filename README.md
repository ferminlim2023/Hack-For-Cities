## Project Description
Introducing *ChatBTO!* Your friendly AI assistant that provides advice for users regarding anything HDB related! 🏠

## Setup Instructions

Step-by-step guide to run the project (dependencies, configurations, etc)

**Assuming user has ollama installed locally**

```
ollama pull granite3.1-dense:3b
```

### For Windows
```
virtualenv .venv
source .venv/bin/activate
```

### For Mac
```
python3.11 -m venv .venv
pip install -r requirements.txt
streamlit run main.py
```

## Usage Guide

Simply start interacting with the AI by talking to it!

Questions you can trying asking are:
- What is the minimum age for a single person to apply for a BTO exercise?
- What kind of documents should I prepare for my HFE letter

### Adding more Information

If you are adding more documents to feed the AI, add them into the "docs" folder and run the following command (make sure you are still in your venv)

### For Window
```
py preprocessing.py
```

### For Mac
```
python3.11 preprocessing.py
```

## Contributors

- Fermin Lim Jun Xian
- Kainoa Ho Wei Jie
- Lee Ka Yong
- Quek De Wang
- Godewyn Goh

## Additional Notes

- AI database is updated as of 11 January 2025