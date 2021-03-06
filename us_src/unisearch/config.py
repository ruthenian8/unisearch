def get_mysql_config(USER, PASSWORD, HOST, PORT, DATABASE, **kwargs) -> str:
    """
    :params: mysql config + arbitrary parameters
    :returns: mysql url
    """
    return "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, HOST, PORT, DATABASE)


CONFIG = {
    "tablename": "chunks",
    "USER": "user",
    "PASSWORD": "qwerty",
    "HOST": "db",
    "PORT": "3306",
    "DATABASE": "db",
}
