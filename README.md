## Project Description
Introducing *ChatBTO!* Your friendly AI assistant that provides advice for users regarding anything HDB related! 🏠

## Setup Instructions

Step-by-step guide to run the project (dependencies, configurations, etc)

**Assuming user has ollama installed locally**

```
ollama pull granite3.1-dense:3b
```

### For Windows
#### DISCLAIMER: U NEED PYTHON VERSION 3.11 TO RUN THIS
```
python -m venv venv
pip install -r requirements.txt
streamlit run main.py
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
Questions you can trying asking are:
- What documents do me and my partner need to submit to apply for the HFE letter?
- Me and my partner are on the deferred income assessment how much would I need to pay for the downpayment, what other payments should I know about and their percentages and which ones are cash or cpf?
- If my partner is currently still in NS, can we still apply for the HFE letter? What documents do we need to prepare?
- Walk me through HFE letter application
- What grants are available for BTO exercise

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