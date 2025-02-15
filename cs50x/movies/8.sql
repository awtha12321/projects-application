--list the names of all people who starred in Toy Story

SELECT people.name
FROM stars
INNER JOIN movies ON movies.id = stars.movie_id
INNER JOIN people ON people.id = stars.person_id
WHERE title = 'Toy Story';