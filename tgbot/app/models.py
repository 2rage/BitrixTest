class Lead:
    def __init__(self, title, comments, lead_id=None, fio='', phone='', email='', status_id='1'):
        self.lead_id = lead_id
        self.title = title
        self.comments = comments
        self.fio = fio
        self.phone = phone
        self.email = email
        self.status_id = status_id
