SELECT AVG(energy)
FROM songs
INNER JOIN artists ON artists.id = songs.artist_id
WHERE artists.id =
    (
        SELECT id
        FROM artists
        WHERE name = 'Drake'
    );