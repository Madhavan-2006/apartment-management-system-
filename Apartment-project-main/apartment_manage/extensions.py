# extensions.py — shared Flask extensions (avoids circular imports)
from flask_mysqldb import MySQL as _MySQL
from flask_login import LoginManager
from flask import g

class PatchedMySQL(_MySQL):
    @property
    def connection(self):
        """
        Attempts to connect to the MySQL server.
        Patched to prevent "NoneType has no attribute cursor" bug
        caused by Flask-MySQLdb's module-level context evaluation.
        """
        try:
            if not hasattr(g, "mysql_db"):
                g.mysql_db = self.connect
            return g.mysql_db
        except RuntimeError:
            # Fallback if accessed outside of app context
            return self.connect

    def teardown(self, exception):
        if hasattr(g, "mysql_db"):
            g.mysql_db.close()

mysql = PatchedMySQL()
login_manager = LoginManager()
