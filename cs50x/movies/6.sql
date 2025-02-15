SELECT AVG(rating)
FROM ratings
JOIN movies
WHERE year = 2012 AND movie_id = id;