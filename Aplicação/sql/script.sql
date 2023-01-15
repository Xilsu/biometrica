CREATE TABLE users (
    username TEXT NOT NULL PRIMARY KEY,
    password TEXT NOT NULL
);

CREATE TABLE roles(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL UNIQUE,
    access_level INTEGER NOT NULL
);

CREATE TABLE employees (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    avatar BLOB,
    role_id INTEGER NOT NULL, 
    FOREIGN KEY (role_id) REFERENCES roles (id)
);

CREATE TABLE templates (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    descriptor TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (id)
);

CREATE TABLE logs (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    authorized INTEGER NOT NULL,
    datetime TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (id)
);

INSERT INTO users VALUES ('admin', 'admin');
INSERT INTO roles (role, access_level) VALUES ('Administrador', 2);