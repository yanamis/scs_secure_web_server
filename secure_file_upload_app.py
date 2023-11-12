#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import tempfile
import secrets
from flask import Flask, request, redirect, session, abort, render_template, Response
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import FileTarget
from werkzeug.utils import secure_filename

# Path to the folder where files will be stored
UPLOAD_FOLDER = "/home/nikosiz/scs_secure_web_server"
# Temporary directory for processing files
MY_UPLOAD_DIR = "/home/nikosiz/scs_secure_web_server/upload"
tempfile.tempdir = MY_UPLOAD_DIR

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'memcached'


@app.before_request
def require_login():
    # Allowed routes that do not require login
    allowed_routes = ['login', 'robots_dot_txt']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')


@app.route("/robots.txt")
def robots_dot_txt():
    # Content of the robots.txt file
    robots_txt = "User-agent: *\r\nDisallow: /"
    return Response(robots_txt, mimetype='text/plain')


@app.route('/')
def index():
    # Display the main page after logging in
    user = session['user']
    return render_template('signed_in.html', user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Check the validity of the request content length
        content_length = int(request.content_length)
        if content_length is not None and content_length > 139:
            return abort(413)
        # Check the provided SHA512 hash for authentication
        provided_hash = request.form['sha512hash']
        if provided_hash == 'fa8c4e2184ce60bedcad15320b91d63557d73e6c52c04540aaa4e3314200ce8e':
            # Set the user session and redirect to the upload page upon successful login
            session['user'] = "ran"
            return redirect('/upload')
        else:
            # Render the error page for unsuccessful login attempts
            return render_template('error.html')
    # Render the login page
    return render_template('authentication.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Generate a random name for the temporary file
        rand_name = "tmp-" + secrets.token_hex(4)
        # Create a target for the file upload
        file_target = FileTarget(os.path.join(tempfile.gettempdir(), rand_name))
        # Create a parser for streaming form data
        parser = StreamingFormDataParser(headers=request.headers)
        parser.register('file', file_target)
        while True:
            # Read the request stream in chunks and process the data
            chunk = request.stream.read(8192)
            if not chunk:
                break
            parser.data_received(chunk)
        # Process the uploaded file
        old_file_path = os.path.join(MY_UPLOAD_DIR, rand_name)
        final_filename = secure_filename(file_target.multipart_filename)
        if not final_filename:
            # Remove the temporary file if no valid filename is provided
            os.remove(old_file_path)
            return render_template('file_missing.html')
        new_file_path = os.path.join(MY_UPLOAD_DIR, final_filename)
        os.rename(old_file_path, new_file_path)
        return render_template("upload_success.html")
    # Render the file upload page for GET requests
    return render_template('file_upload.html')


@app.route('/logout')
def logout():
    # Clear the user session and redirect to the main page
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
