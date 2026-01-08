# [Income-Tax-Estimator](https://github.com/rweastman-lgtm/Income-Tax-Estimator)
Tax and Conversion and Withdrawal 
- uses [Streamlit](https://pypi.org/project/streamlit/)  
  - `streamlit run Tax_estimator_app.py`  

## [Windows 11 Python](https://windowsforum.com/threads/best-ways-to-install-python-on-windows-11-expert-tips-methods.374218/) and [Streamlit](https://pypi.org/project/streamlit/) installation  
- [Python install manager](https://docs.python.org/dev/using/windows.html)  
	- installs only python *versions*, not *packages*  
	- allow paths longer than 260 chars
	- adds to PATH: `%USERPROFILE%\AppData\Local\Python\bin`
	- installed 3.14.2 "To see all available commands, run 'py help'"
- [manually add to PATH](https://geekrewind.com/how-to-add-and-edit-path-environment-variables-in-windows-11/):
	- `%USERPROFILE%\AppData\Local\Python\pythoncore-3.14-64\Scripts`
- **install streamlit**
	- `python -m pip install streamlit`
