class File:
    fileName = None

    def __init__(self, title: str):
        """
        generates valid fileName from steam workshop title

        original code: https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
        """
        import unicodedata
        import string

        valid_filename_chars = "-_.[]() %s%s" % (string.ascii_letters, string.digits)
        for r in " ":
            title = title.replace(r, "_")
        self.fileName = (
            unicodedata.normalize("NFKD", title).encode("ASCII", "ignore").decode()
        )
        self.fileName = "".join(c for c in self.fileName if c in valid_filename_chars)
        self.fileName = self.fileName[:255]
