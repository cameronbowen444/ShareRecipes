from flask_app.config.mysqlconnection import connectToMySQL


def initialize_database():
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INT NOT NULL AUTO_INCREMENT,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
    );
    """

    create_recipes_table = """
    CREATE TABLE IF NOT EXISTS recipes (
        id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        instructions TEXT NOT NULL,
        date DATE NOT NULL,
        under30 TINYINT NOT NULL DEFAULT 0,
        user_id INT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        CONSTRAINT fk_recipes_users
            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
    );
    """

    connectToMySQL("real_recipes").query_db(create_users_table)
    connectToMySQL("real_recipes").query_db(create_recipes_table)