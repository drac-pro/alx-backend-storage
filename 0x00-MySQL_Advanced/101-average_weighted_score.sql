-- creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done TINYINT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE average FLOAT;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
        INTO average FROM corrections 
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id=user_id;
        UPDATE users SET average_score=average WHERE id=user_id;
    END LOOP;

    CLOSE cur;
END $$
DELIMITER ;
