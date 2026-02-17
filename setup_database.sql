-- Run this as postgres superuser or ask your hosting provider to execute it

-- Grant permissions to dbadmin
ALTER SCHEMA public OWNER TO dbadmin;
GRANT ALL PRIVILEGES ON SCHEMA public TO dbadmin;
GRANT CREATE ON SCHEMA public TO dbadmin;

-- Create tables
CREATE TABLE IF NOT EXISTS admins (
    id SERIAL NOT NULL,
    email VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE UNIQUE INDEX IF NOT EXISTS ix_admins_email ON admins (email);

CREATE TABLE IF NOT EXISTS token_blacklist (
    id SERIAL NOT NULL,
    token VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE UNIQUE INDEX IF NOT EXISTS ix_token_blacklist_token ON token_blacklist (token);

CREATE TABLE IF NOT EXISTS members (
    id SERIAL NOT NULL,
    membership_id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    phone VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    aadhaar VARCHAR NOT NULL,
    blood_group VARCHAR,
    designation VARCHAR,
    father_husband_name VARCHAR,
    state VARCHAR NOT NULL,
    district VARCHAR NOT NULL,
    mandal VARCHAR NOT NULL,
    village VARCHAR,
    full_address TEXT,
    status VARCHAR DEFAULT 'pending',
    is_active BOOLEAN DEFAULT true,
    id_card_generated BOOLEAN DEFAULT false,
    photo_path VARCHAR,
    qr_code_path VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE UNIQUE INDEX IF NOT EXISTS ix_members_membership_id ON members (membership_id);
CREATE INDEX IF NOT EXISTS ix_members_name ON members (name);
CREATE INDEX IF NOT EXISTS ix_members_phone ON members (phone);
CREATE INDEX IF NOT EXISTS ix_members_email ON members (email);
CREATE INDEX IF NOT EXISTS ix_members_aadhaar ON members (aadhaar);
CREATE INDEX IF NOT EXISTS ix_members_state ON members (state);
CREATE INDEX IF NOT EXISTS ix_members_district ON members (district);
CREATE INDEX IF NOT EXISTS ix_members_mandal ON members (mandal);
CREATE INDEX IF NOT EXISTS ix_members_status ON members (status);

CREATE TABLE IF NOT EXISTS member_applications (
    id SERIAL NOT NULL,
    full_name VARCHAR,
    father_husband_name VARCHAR,
    gender VARCHAR,
    date_of_birth DATE,
    caste VARCHAR,
    aadhaar_number VARCHAR,
    phone_number VARCHAR,
    email_address VARCHAR,
    blood_group VARCHAR,
    designation VARCHAR,
    state VARCHAR,
    district VARCHAR,
    mandal VARCHAR,
    village VARCHAR,
    full_address TEXT,
    photo_path VARCHAR,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_member_applications_full_name ON member_applications (full_name);
CREATE INDEX IF NOT EXISTS ix_member_applications_aadhaar_number ON member_applications (aadhaar_number);
CREATE INDEX IF NOT EXISTS ix_member_applications_phone_number ON member_applications (phone_number);
CREATE INDEX IF NOT EXISTS ix_member_applications_status ON member_applications (status);

CREATE TABLE IF NOT EXISTS donations (
    id SERIAL NOT NULL,
    donor_name VARCHAR,
    donor_email VARCHAR,
    phone_number VARCHAR,
    amount FLOAT,
    payment_method VARCHAR,
    transaction_id VARCHAR,
    notes TEXT,
    status VARCHAR DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_donations_donor_name ON donations (donor_name);
CREATE INDEX IF NOT EXISTS ix_donations_donor_email ON donations (donor_email);
CREATE INDEX IF NOT EXISTS ix_donations_transaction_id ON donations (transaction_id);
CREATE INDEX IF NOT EXISTS ix_donations_status ON donations (status);

CREATE TABLE IF NOT EXISTS complaints (
    id SERIAL NOT NULL,
    complainant_name VARCHAR NOT NULL,
    email VARCHAR,
    phone VARCHAR NOT NULL,
    address TEXT NOT NULL,
    type VARCHAR NOT NULL,
    subject VARCHAR NOT NULL,
    description TEXT NOT NULL,
    reference_id VARCHAR NOT NULL,
    supporting_document_path VARCHAR,
    status VARCHAR DEFAULT 'pending',
    admin_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE UNIQUE INDEX IF NOT EXISTS ix_complaints_reference_id ON complaints (reference_id);
CREATE INDEX IF NOT EXISTS ix_complaints_complainant_name ON complaints (complainant_name);
CREATE INDEX IF NOT EXISTS ix_complaints_email ON complaints (email);
CREATE INDEX IF NOT EXISTS ix_complaints_type ON complaints (type);
CREATE INDEX IF NOT EXISTS ix_complaints_subject ON complaints (subject);
CREATE INDEX IF NOT EXISTS ix_complaints_status ON complaints (status);

CREATE TABLE IF NOT EXISTS gallery (
    id SERIAL NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT,
    media_url VARCHAR NOT NULL,
    media_type VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_gallery_title ON gallery (title);
CREATE INDEX IF NOT EXISTS ix_gallery_media_type ON gallery (media_type);

-- Grant all privileges on tables to dbadmin
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dbadmin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dbadmin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO dbadmin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO dbadmin;
