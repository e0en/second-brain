CREATE TABLE entry (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tag (
    name TEXT NOT NULL UNIQUE PRIMARY KEY,
    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE entry_tag (
    entry_id INTEGER NOT NULL,
    tag_name TEXT NOT NULL,
    FOREIGN KEY (entry_id)
        REFERENCES entry (id),
    FOREIGN KEY (tag_name)
        REFERENCES tag (name)
);

CREATE TABLE access_log (
    entry_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);
