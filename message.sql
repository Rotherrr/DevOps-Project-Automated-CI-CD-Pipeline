-- Runs once, on the first start of an empty MySQL data volume.
CREATE DATABASE IF NOT EXISTS devops;
USE devops;

CREATE TABLE IF NOT EXISTS messages (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    message    VARCHAR(255) NOT NULL,
    created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO messages (message) VALUES
    ('Hello from MySQL! This row was created by message.sql.'),
    ('If you can read this, Flask and the database are talking to each other.');
