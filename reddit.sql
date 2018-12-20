-- total number of comments

select count(*)
from myredditcomments;

-- general sentiment of reddit Today

select round(avg(pattern_polarity), 4) as avg_polarity
from myredditcomments
where r_date
like '%${today}%'; -- YYYY-MM-DD

-- total comments collected per subreddits

select count(*) as num_comments, subreddit
from myredditcomments
group by subreddit;

-- average pattern polarity analysis per subreddits

select round(avg(pattern_polarity), 4) as avg_pattern_polarity, subreddit
from myredditcomments
group by subreddit;


-- most positive authors with more than 20 comments

select count(*) as num_comments, author, round(avg(pattern_polarity), 4) as avg_polarity
from myredditcomments
group by author
having count(*) > 20
order by avg_polarity DESC;

-- insight into most positive authors

select *
from myredditcomments
where author = '${author}';

-- average naives bayes positive analysis per subreddit

select round(avg(naivesbayes_positive), 4) as avg_naivesbayes, subreddit
from myredditcomments
group by subreddit;

-- most positive authors with more than 20 comments

select count(*) as num_comments, author, round(avg(naivesbayes_positive), 4) as avg_naivesbayes_positive
from myredditcomments
group by author
having count(*) > 20
order by avg_naivesbayes_positive DESC;

-- insight into most positive author

select author, subreddit, r_comment, naivesbayes_positive, pattern_polarity
from myredditcomments
where author = '${author}';

-- most active Users

select author, count(*) as num_comments
from myredditcomments
group by author
order by num_comments DESC;

-- insight into most active users:

select *
from myredditcomments
where author = '${author}';

-- list all Subreddits

select distinct(subreddit)
from myredditcomments;

-- top 10 most negative comments by subreddit

select subreddit, author, r_comment
from
    (select *
     from myredditcomments
     where subreddit = '${subreddit}'
     order by pattern_polarity ASC)
where ROWNUM < 10

-- top 10 most positive comments by subreddit

select subreddit, author, r_comment
from
    (select *
     from myredditcomments
     where subreddit = '${subreddit}'
     order by pattern_polarity DESC)
where ROWNUM < 10


-- most active subreddits

select subreddit, count(*) as num_comments, round(avg(pattern_polarity), 4) as avg_polarity, round(avg(naivesbayes_positive), 4) as avg_naivesbayes
from myredditcomments
group by subreddit
order by num_comments DESC;





-- search term frequency by subreddit where comments greater than 5

select subreddit, count(*) as occurrences
 from myredditcomments 
 where LOWER(r_comment) like '%${lowercase term}%'
group by subreddit
having count(*) > 5
order by occurrences desc;






-- subreddit sentiment on search term

select subreddit, round(avg(pattern_polarity), 4) as avg_polarity
 from myredditcomments 
 where LOWER(r_comment) like '%${lowercase term}%'
group by subreddit
having count(*) > 5
order by avg_polarity desc;



-- top 25 most negative comments about a search term

SELECT * FROM( 
 SELECT subreddit, author, r_comment, pattern_polarity, naivesbayes_positive 
 FROM myredditcomments 
 WHERE LOWER(r_comment) LIKE '%${lowercase term}%'
 ORDER BY pattern_polarity ASC)
 WHERE ROWNUM <= 25
 
 
 -- top 25 most positive comments about a search term
 
 SELECT * FROM( 
 SELECT subreddit, author, r_comment, pattern_polarity, naivesbayes_positive 
 FROM myredditcomments 
 WHERE LOWER(r_comment) LIKE '%${lowercase term}%'
 ORDER BY pattern_polarity DESC)
 WHERE ROWNUM <= 25
 
 
 -- comparing search terms for sentiment
 
 SELECT round(avg(pattern_polarity), 4) as avg_polarity, round(avg(naivesbayes_positive), 4) as avg_naivesbayes 
FROM ( 
 SELECT subreddit, author, r_comment, pattern_polarity, naivesbayes_positive 
 FROM myredditcomments 
 WHERE LOWER(r_comment) LIKE '%${lowercase term}%')
 
 
 -- search term sentiment over time:
 
 SELECT r_date_formatted, round(avg(pattern_polarity), 4) as avg_polarity
FROM ( 
 SELECT subreddit, author, r_comment, r_date, pattern_polarity,  TO_CHAR(TO_DATE(r_date,'YYYY-MM-DD HH24:MI:SS'), 'YYYY-MM-DD')  as r_date_formatted 
 FROM myredditcomments 
 WHERE LOWER(r_comment) LIKE '%${lowercase term}%')
GROUP BY r_date_formatted
ORDER BY r_date_formatted ASC
 