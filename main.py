from login_page import LoginPage
from app_configs import init_app

def main():
    root_window = init_app()
    LoginPage()
    root_window.mainloop()

if __name__ == "__main__":
    main()