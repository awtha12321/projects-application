--list the names of all people who have directed a movie that received a rating of at least 9.0

SELECT DISTINCT people.name
FROM directors
INNER JOIN people ON people.id = directors.person_id
INNER JOIN ratings ON ratings.movie_id = directors.movie_id
WHERE rating >= 9.0;