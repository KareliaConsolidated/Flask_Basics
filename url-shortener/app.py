from flask import Flask, render_template, request, redirect, url_for, flash, abort
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'kareliaconsolidated'

@app.route('/')

def home():
	return render_template('home.html')

@app.route('/about')	

def about():
	return 'This is a URL Shortener'


@app.route('/your-url', methods=['GET','POST'])	

def your_url():
	if request.method == 'POST':
		urls = {}
		# Check if url and code exist in urls.json
		if os.path.exists('urls.json'):
			with open('urls.json') as urls_file:
				urls = json.load(urls_file)
		# If url and code exists, redirect it to home				
		if request.form['code'] in urls.keys():
			flash('That Short Name has already been taken. Please select another name.')
			return redirect(url_for('home'))

		# To Check if its url or a file
		if 'url' in request.form.keys():
			urls[request.form['code']] = {'url': request.form['url']}
		else:
			f = request.files['file']
			full_name = request.form['code'] + secure_filename(f.filename)
			f.save('E:/Project/Flask Basics/url-shortener/static/user_files/' + full_name)
			urls[request.form['code']] = {'file': full_name}

		with open('urls.json','w') as url_file:
			json.dump(urls, url_file)

		return render_template('your_url.html', code = request.form['code'])
	else:
		return redirect(url_for('home')) # Provided Name of the Function i.e. home

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404