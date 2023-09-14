@ECHO OFF
python.exe -m pip install -r requirements.txt
sbase get chromedriver
sbase get uc_driver
call streamlit run panel.py