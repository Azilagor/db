CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE experience_level (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(20) NOT NULL,
    level_number    INT NOT NULL CHECK (level_number > 0),
    description     TEXT,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_experience_level_name UNIQUE (name),
    CONSTRAINT chk_experience_level_name CHECK (name IN ('beginner', 'intermediate', 'expert'))
);

CREATE TABLE tourist (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    level_id        UUID NOT NULL,
    full_name       VARCHAR(100) NOT NULL,
    passport_data   VARCHAR(50) NOT NULL,
    email           VARCHAR(100),
    gender          CHAR(1),
    age             INT,
    experience      TEXT,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_tourist_level FOREIGN KEY (level_id) REFERENCES experience_level(id),
    CONSTRAINT uq_tourist_full_name UNIQUE (full_name),
    CONSTRAINT uq_tourist_passport UNIQUE (passport_data),
    CONSTRAINT uq_tourist_email UNIQUE (email),
    CONSTRAINT chk_tourist_gender CHECK (gender IN ('M', 'F')),
    CONSTRAINT chk_tourist_age CHECK (age > 0 AND age < 120)
);

CREATE TABLE guide (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    level_id        UUID NOT NULL,
    full_name       VARCHAR(100) NOT NULL,
    passport_data   VARCHAR(50) NOT NULL,
    phone           VARCHAR(20),
    age             INT,
    hike_count      INT NOT NULL DEFAULT 0,
    can_drive       BOOLEAN NOT NULL DEFAULT FALSE,
    can_raft        BOOLEAN NOT NULL DEFAULT FALSE,
    experience      TEXT,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_guide_level FOREIGN KEY (level_id) REFERENCES experience_level(id),
    CONSTRAINT uq_guide_full_name UNIQUE (full_name),
    CONSTRAINT uq_guide_passport UNIQUE (passport_data),
    CONSTRAINT chk_guide_age CHECK (age > 0 AND age < 120),
    CONSTRAINT chk_guide_hike_count CHECK (hike_count >= 0)
);

CREATE TABLE season (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name                    VARCHAR(20) NOT NULL,
    start_date              DATE NOT NULL,
    end_date                DATE NOT NULL,
    extremality_influence   DECIMAL(4,2),
    active                  BOOLEAN NOT NULL DEFAULT TRUE,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_season_name UNIQUE (name),
    CONSTRAINT chk_season_name CHECK (name IN ('spring', 'summer', 'autumn', 'winter')),
    CONSTRAINT chk_season_dates CHECK (end_date > start_date)
);

CREATE TABLE route (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    level_id        UUID NOT NULL,
    name            VARCHAR(100) NOT NULL,
    start_point     VARCHAR(100) NOT NULL,
    end_point       VARCHAR(100) NOT NULL,
    length_km       DECIMAL(6,2),
    travel_type     VARCHAR(20),
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_route_level FOREIGN KEY (level_id) REFERENCES experience_level(id),
    CONSTRAINT uq_route_name UNIQUE (name),
    CONSTRAINT chk_route_length CHECK (length_km > 0),
    CONSTRAINT chk_route_travel_type CHECK (travel_type IN ('hiking', 'rafting', 'car', 'snowmobile'))
);

CREATE TABLE route_point (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    route_id            UUID NOT NULL,
    name                VARCHAR(100) NOT NULL,
    latitude            DECIMAL(9,6) NOT NULL,
    longitude           DECIMAL(9,6) NOT NULL,
    short_description   TEXT,
    purpose             VARCHAR(50),
    active              BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_route_point_route FOREIGN KEY (route_id) REFERENCES route(id),
    CONSTRAINT uq_route_point_name UNIQUE (name),
    CONSTRAINT chk_route_point_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT chk_route_point_longitude CHECK (longitude BETWEEN -180 AND 180),
    CONSTRAINT chk_route_point_purpose CHECK (purpose IN ('rest', 'overnight', 'pass', 'excursion'))
);

CREATE TABLE inventory (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(100) NOT NULL,
    type            VARCHAR(50),
    size            VARCHAR(10),
    weight_kg       DECIMAL(5,2),
    volume_l        DECIMAL(5,2),
    rental_cost     DECIMAL(10,2) NOT NULL,
    stock_quantity  INT NOT NULL DEFAULT 0,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_inventory_name UNIQUE (name),
    CONSTRAINT chk_inventory_size CHECK (size IN ('small', 'medium', 'large')),
    CONSTRAINT chk_inventory_weight CHECK (weight_kg IS NULL OR weight_kg >= 0),
    CONSTRAINT chk_inventory_volume CHECK (volume_l IS NULL OR volume_l >= 0),
    CONSTRAINT chk_inventory_rental_cost CHECK (rental_cost >= 0),
    CONSTRAINT chk_inventory_stock CHECK (stock_quantity >= 0)
);

CREATE TABLE transport (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name             VARCHAR(100) NOT NULL,
    kind             VARCHAR(50),
    capacity         INT,
    luggage_volume_l DECIMAL(7,2),
    cost             DECIMAL(10,2),
    service_cost     DECIMAL(10,2),
    ownership_type   VARCHAR(20),
    active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_transport_name UNIQUE (name),
    CONSTRAINT chk_transport_capacity CHECK (capacity > 0),
    CONSTRAINT chk_transport_cost CHECK (cost IS NULL OR cost >= 0),
    CONSTRAINT chk_transport_service_cost CHECK (service_cost IS NULL OR service_cost >= 0),
    CONSTRAINT chk_transport_ownership CHECK (ownership_type IN ('own', 'rented'))
);

CREATE TABLE hike (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    route_id    UUID NOT NULL,
    start_date  DATE NOT NULL,
    end_date    DATE,
    status      VARCHAR(20) NOT NULL DEFAULT 'planned',
    cost        DECIMAL(10,2),
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_hike_route FOREIGN KEY (route_id) REFERENCES route(id),
    CONSTRAINT chk_hike_dates CHECK (end_date IS NULL OR end_date >= start_date),
    CONSTRAINT chk_hike_status CHECK (status IN ('planned', 'started', 'completed', 'cancelled')),
    CONSTRAINT chk_hike_cost CHECK (cost IS NULL OR cost >= 0)
);

CREATE TABLE trail_book (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hike_id     UUID NOT NULL,
    start_date  DATE,
    end_date    DATE,
    status      VARCHAR(20),
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_trail_book_hike FOREIGN KEY (hike_id) REFERENCES hike(id),
    CONSTRAINT uq_trail_book_hike UNIQUE (hike_id),
    CONSTRAINT chk_trail_book_dates CHECK (end_date IS NULL OR end_date >= start_date),
    CONSTRAINT chk_trail_book_status CHECK (status IN ('planned', 'started', 'completed', 'cancelled'))
);

CREATE TABLE tourist_hike (
    tourist_id  UUID NOT NULL,
    hike_id     UUID NOT NULL,
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (tourist_id, hike_id),
    CONSTRAINT fk_tourist_hike_tourist FOREIGN KEY (tourist_id) REFERENCES tourist(id),
    CONSTRAINT fk_tourist_hike_hike FOREIGN KEY (hike_id) REFERENCES hike(id)
);

CREATE TABLE guide_hike (
    hike_id     UUID NOT NULL,
    guide_id    UUID NOT NULL,
    role        VARCHAR(20) NOT NULL DEFAULT 'lead',
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (hike_id, guide_id),
    CONSTRAINT fk_guide_hike_hike FOREIGN KEY (hike_id) REFERENCES hike(id),
    CONSTRAINT fk_guide_hike_guide FOREIGN KEY (guide_id) REFERENCES guide(id),
    CONSTRAINT chk_guide_hike_role CHECK (role IN ('lead', 'assistant'))
);

CREATE TABLE route_season (
    route_id    UUID NOT NULL,
    season_id   UUID NOT NULL,
    scenery     VARCHAR(50),
    extremality VARCHAR(50),
    cost        DECIMAL(10,2),
    active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (route_id, season_id),
    CONSTRAINT fk_route_season_route FOREIGN KEY (route_id) REFERENCES route(id),
    CONSTRAINT fk_route_season_season FOREIGN KEY (season_id) REFERENCES season(id),
    CONSTRAINT chk_route_season_cost CHECK (cost IS NULL OR cost >= 0)
);

CREATE TABLE route_point_season (
    route_point_id  UUID NOT NULL,
    season_id       UUID NOT NULL,
    scenery         VARCHAR(50),
    extremality     VARCHAR(50),
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (route_point_id, season_id),
    CONSTRAINT fk_rps_route_point FOREIGN KEY (route_point_id) REFERENCES route_point(id),
    CONSTRAINT fk_rps_season FOREIGN KEY (season_id) REFERENCES season(id)
);

CREATE TABLE hike_inventory (
    hike_id         UUID NOT NULL,
    inventory_id    UUID NOT NULL,
    quantity        INT NOT NULL DEFAULT 1,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (hike_id, inventory_id),
    CONSTRAINT fk_hike_inventory_hike FOREIGN KEY (hike_id) REFERENCES hike(id),
    CONSTRAINT fk_hike_inventory_inventory FOREIGN KEY (inventory_id) REFERENCES inventory(id),
    CONSTRAINT chk_hike_inventory_quantity CHECK (quantity > 0)
);

CREATE TABLE hike_transport (
    hike_id         UUID NOT NULL,
    transport_id    UUID NOT NULL,
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (hike_id, transport_id),
    CONSTRAINT fk_hike_transport_hike FOREIGN KEY (hike_id) REFERENCES hike(id),
    CONSTRAINT fk_hike_transport_transport FOREIGN KEY (transport_id) REFERENCES transport(id)
);