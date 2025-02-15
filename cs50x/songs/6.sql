SELECT songs.name
FROM songs
INNER JOIN artists ON artists.id = songs.artist_id
WHERE artists.id =
    (
        SELECT id
        FROM artists
        WHERE name = 'Post Malone'
    );