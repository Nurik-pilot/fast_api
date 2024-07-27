CREATE OR REPLACE FUNCTION snapshot_after_insert_on_{lower_target}()
RETURNS TRIGGER AS $snapshot_after_insert_on_{lower_target}$
BEGIN
    INSERT INTO "{target}"
    (id, created_at, snapshot_type, data)
    VALUES
    (
        gen_random_uuid(),
        statement_timestamp(),
        'after_inserted',
        row_to_json(NEW)
    );
    RETURN NEW;
END;
$snapshot_after_insert_on_{lower_target}$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS snapshot_after_insert_on_{lower_target} on "{source}";
CREATE TRIGGER snapshot_after_insert_on_{lower_target}
AFTER INSERT ON "{source}"
FOR EACH ROW EXECUTE PROCEDURE snapshot_after_insert_on_{lower_target}();

CREATE OR REPLACE FUNCTION snapshot_after_update_on_{lower_target}()
RETURNS TRIGGER AS $snapshot_after_update_on_{lower_target}$
BEGIN
    INSERT INTO "{target}"
    (id, created_at, snapshot_type, data)
    VALUES
    (
        gen_random_uuid(),
        statement_timestamp(),
        'after_updated',
        row_to_json(NEW)
    );
    RETURN NEW;
END;
$snapshot_after_update_on_{lower_target}$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS snapshot_after_update_on_{lower_target} on "{source}";
CREATE TRIGGER snapshot_after_update_on_{lower_target}
AFTER UPDATE ON "{source}"
FOR EACH ROW EXECUTE PROCEDURE snapshot_after_update_on_{lower_target}();

CREATE OR REPLACE FUNCTION snapshot_before_delete_on_{lower_target}()
RETURNS TRIGGER AS $snapshot_before_delete_on_{lower_target}$
BEGIN
    INSERT INTO "{target}"
    (id, created_at, snapshot_type, data)
    VALUES
    (
        gen_random_uuid(),
        statement_timestamp,
        'before_deleted',
        row_to_json(OLD)
    );
    RETURN OLD;
END;
$snapshot_before_delete_on_{lower_target}$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS snapshot_before_delete_on_{lower_target} on "{source}";
CREATE TRIGGER snapshot_before_delete_on_{lower_target}
BEFORE DELETE ON "{source}"
FOR EACH ROW EXECUTE PROCEDURE snapshot_before_delete_on_{lower_target}();
