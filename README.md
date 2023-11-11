# Secure Web Server

This project uses **Flask** in conjunction with **uWSGI** and **Werkzeug**. The **streaming-form-data** library is employed for handling streaming form data.

## Dependencies

Ensure that you have installed the required dependencies using pip:

```bash
pip install Flask uWSGI Werkzeug streaming-form-data
```

## How to Launch the Server

To start the server, use the following command with uWSGI:
```bash
uwsgi --ini uwsgi.ini
```

This command will initiate the server, and you can access the application through your web browser.

Remember to tailor the **uwsgi.ini** file according to your project configuration.

## Additional Notes
* This project assumes the use of **Python 3**.
* For any issues, refer to the documentation of **Flask**, **uWSGI**, **Werkzeug**, and **streaming-form-data**.
