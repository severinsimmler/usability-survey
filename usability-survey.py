import application
import webbrowser


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    application.views.web.run(debug=True)
