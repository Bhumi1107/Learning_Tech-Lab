WITH copy_status AS (
    SELECT c.book_id,
           EXISTS (
               SELECT 1
               FROM loans AS l
               WHERE l.copy_id = c.id
                 AND l.borrowed_on <= :day
                 AND (l.returned_on IS NULL OR l.returned_on > :day)
           ) AS on_loan
    FROM copies AS c
)
SELECT b.title,
       COUNT(s.book_id) AS total,
       COALESCE(SUM(s.on_loan), 0) AS on_loan,
       COUNT(s.book_id) - COALESCE(SUM(s.on_loan), 0) AS available
FROM books AS b
LEFT JOIN copy_status AS s ON s.book_id = b.id
GROUP BY b.id, b.title
ORDER BY b.title, b.id;
