class DatabaseConfig:
    USER: str = "root"
    PASSWORD: str = "root"
    HOST: str = "localhost"  # 127.0.0.1:3306
    PORT: str = "3306"
    DATABASE: str = "streak"
    CONNECTION_STRING = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}"

    def get_config(self):
        return {
            "user": self.USER,
            "password": self.PASSWORD,
            "host": self.HOST,
            "database": self.DATABASE,
            "raise_on_warnings": True,
        }
