DO $$
BEGIN
 IF NOT EXISTS(SELECT FROM pg_database WHERE datname = 'courseservice') THEN
    CREATE DATABASE courseservice;
    GRANT ALL PRIVILEGES ON DATABASE courseservice TO postgres;
 END IF;
END $$;
