    CREATE OR REPLACE FUNCTION trigger_set_timestamp()
    RETURNS TRIGGER AS $$
    BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE TABLE IF NOT EXISTS ksb(
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        ksb_type   VARCHAR(9)    NOT NULL,
        ksb_code   INT    NOT NULL,
        description TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    
    CREATE TRIGGER set_timestamp
    BEFORE UPDATE ON ksb
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_timestamp();

    INSERT INTO ksb (ksb_type, ksb_code, description)
    VALUES  ('Knowledge', 5, 'Modern security tools and techniques, including threat modelling and vulnerability scanning.'),  
            ('Knowledge', 7, 'General purpose programming and infrastructure-as-code.'),  
            ('Skill', 9, 'Using cloud security tools and automating security in pipelines.'),  
            ('Behaviour', 3, 'Takes ownership of deployed code and learns from failures.');  