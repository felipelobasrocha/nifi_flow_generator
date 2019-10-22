


def login(self, email, password):
    return self.app.post(
        '/login',
        data=dict(email=email, password=password),
        follow_redirects=True
    )