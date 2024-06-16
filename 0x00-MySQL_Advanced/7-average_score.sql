-- Script that creates a stored procedure ComputeAverageScoreForUser that computes
-- and store the average score for a student.
-- Note: An average score can be a decimal.

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;

    -- Compute the total score for the user
    SELECT SUM(score) INTO total_score
    FROM corrections
    WHERE corrections.user_id = user_id;

    -- Compute number of projects
    SELECT COUNT(*) INTO total_projects
    FROM corrections
    WHERE corrections.user_id = user_id;

    UPDATE users
        SET users.average_score = IF(total_projects = 0, 0, total_score / total_projects)
        WHERE users.id = user_id;

END$$

DELIMITER ;