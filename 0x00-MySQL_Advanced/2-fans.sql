-- Script to rank country origins of bands based on the number of (non-unique) fans.
-- The script assumes the existence of a table named 'metal_bands' with appropriate data.
-- It outputs the origin and the total number of fans for each origin, ordered by the number of fans in descending order.

SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;