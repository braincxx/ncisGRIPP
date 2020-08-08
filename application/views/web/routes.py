from app_instance import app
from .index import IndexView
from .profile import ProfileView


@app.route('/')
def index():
    return IndexView.index()


# @app.route('/map')
# def virus_map():
#     return IndexView.map()


@app.route('/map')
def virus_map():
    return IndexView.map()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return IndexView.login()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return IndexView.register()


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return IndexView.dashboard()


@app.route('/logout')
def logout():
    return IndexView.logout()


@app.route('/actions')
def actions():
    return IndexView.actions()


@app.route('/news')
def news():
    return IndexView.news()


@app.route('/about')
def about():
    return IndexView.about()


@app.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
    return ProfileView.edit()


@app.route('/profile/tokens/generate', methods=['GET'])
def profile_generate_token():
    return ProfileView.generate_token()


@app.route('/profile/tokens/delete/<int:token_id>')
def profile_delete_token(token_id: int):
    return ProfileView.delete_token(token_id)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return ProfileView.index()
