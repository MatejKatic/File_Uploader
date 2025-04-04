CREATE TABLE uploads (
  id SERIAL PRIMARY KEY,
  uuid UUID NOT NULL UNIQUE,
  filename VARCHAR(255) NOT NULL,
  file_data BYTEA NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- index on uuid for faster lookups
CREATE INDEX idx_uploads_uuid ON uploads(uuid);