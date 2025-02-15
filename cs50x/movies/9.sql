--uery to list the names of all people who starred in a movie released in 2004, ordered by birth year

SELECT people.name
FROM stars
INNER JOIN movies ON movies.id = stars.movie_id
INNER JOIN people ON people.id = stars.person_id
WHERE year = 2004
GROUP BY name, person_id
ORDER BY birth;