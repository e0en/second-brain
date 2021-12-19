CREATE TABLE entry (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tag (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE entry_tag (
    entry_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (entry_id)
        REFERENCES entry (id),
    FOREIGN KEY (tag_id)
        REFERENCES tag (id)
);

CREATE TABLE access_log (
    entry_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);
