-- Script that creates a view need_meeting that lists all students
-- that have a score under 80 (strict) and no last_meeting or more than 1 month.

CREATE VIEW need_meeting AS
    SELECT users.id, users.name, users.last_meeting, users.score
    FROM users
    WHERE users.score < 80
    AND (users.last_meeting IS NULL OR users.last_meeting < DATE_SUB(NOW(), INTERVAL 1 MONTH));