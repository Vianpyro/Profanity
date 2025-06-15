-- Enable foreign key support in SQLite
PRAGMA foreign_keys = ON;
-- Drop existing tables if they exist
DROP TABLE IF EXISTS languages;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS profanities;
DROP TABLE IF EXISTS replacements;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS contextual_rules;
CREATE TABLE languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    english_name TEXT NOT NULL UNIQUE,
    native_name TEXT,
    iso_code TEXT NOT NULL UNIQUE
);
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    category_description TEXT
);
CREATE TABLE profanities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profanity_name TEXT NOT NULL UNIQUE,
    language_id INTEGER NOT NULL,
    category_id INTEGER,
    severity_level TEXT CHECK (
        severity_level IN ('mild', 'moderate', 'severe', 'unknown')
    ) DEFAULT 'unknown',
    is_phrase BOOLEAN NOT NULL DEFAULT 0,
    context_hint TEXT,
    created_by_user BOOLEAN NOT NULL DEFAULT 1,
    is_enabled BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (language_id) REFERENCES languages (id),
    FOREIGN KEY (category_id) REFERENCES categories (id)
);
CREATE TABLE replacements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profanity_id INTEGER NOT NULL,
    replacement_text TEXT,
    note TEXT,
    FOREIGN KEY (profanity_id) REFERENCES profanities (id)
);
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    project_id INTEGER,
    input_text TEXT NOT NULL,
    result_text TEXT NOT NULL,
    -- JSON or comma-separated
    detected_words TEXT,
    ip_address TEXT,
    user_agent TEXT,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);
CREATE TABLE contextual_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profanity_id INTEGER NOT NULL,
    rule_name TEXT NOT NULL,
    rule_type TEXT NOT NULL CHECK (
        rule_type IN (
            'before',
            'after',
            'within',
            'regex',
            'pattern',
            'only'
        )
    ) DEFAULT 'within',
    pattern TEXT,
    is_safe BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (profanity_id) REFERENCES profanities (id)
);
