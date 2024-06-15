-- Script to list all bands with Glam rock as their main style, ranked by their longevity.
-- The script assumes the existence of a table named 'metal_bands' with appropriate data.
-- The lifespan is calculated based on the 'formed' and 'split' attributes, assuming 2022 as the current year if 'split' is NULL.

SELECT 
    band_name, 
    CASE 
        WHEN split IS NULL THEN 2022 - formed
        ELSE split - formed
    END AS lifespan
FROM 
    metal_bands
WHERE 
    style LIKE '%Glam rock%'
ORDER BY 
    lifespan DESC;
