CREATE TABLE IF NOT EXISTS scrap_requests (
    id SERIAL PRIMARY KEY,
    status VARCHAR(32) NOT NULL DEFAULT 'open',
    scrap_type VARCHAR(64) NOT NULL,
    estimated_price NUMERIC(12,2) NOT NULL,
    geo_point JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS saleng_locations (
    id SERIAL PRIMARY KEY,
    saleng_id VARCHAR(64) NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    long DOUBLE PRECISION NOT NULL,
    accuracy DOUBLE PRECISION,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS verification_records (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(32) NOT NULL,
    method VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL,
    verified_at TIMESTAMPTZ
);
