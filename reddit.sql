
-- average sentiment by subreddit
select round(avg(naivesbayes_positive), 4), subreddit from redditcomments group by subreddit;
select round(avg(pattern_polarity), 4), subreddit from redditcomments group by subreddit;

-- total number of comments for each subreddit
select count(*), subreddit from redditcomments group by subreddit;


-- most pattern_polarity authors 
select round(avg(pattern_polarity), 4) as avg_polarity, author 
from redditcomments
group by author 
order by avg_polarity DESC;


-- find average pattern polarity for authors with at least 5 comments
select count(*) as num_comments, author, round(avg(pattern_polarity), 4) as avg_polarity from redditcomments group by author having count(*) > 5 order by avg_polarity DESC; 


-- find average naivesbayes_positive for authors with at least 5 comments
select count(*) as num_comments, author, round(avg(naivesbayes_positive), 4) as avg_naivesbayes_positive from redditcomments group by author having count(*) > 5 order by avg_naivesbayes_positive DESC; 


-- most naivesbayes_positive authors 
select round(avg(naivesbayes_positive), 4) as avg_naivesbayes_positive, author 
from redditcomments 
group by author 
order by avg_naivesbayes_positive DESC;

-- find most active authors
select author, count(*) as num_comments from redditcomments group by author order by num_comments DESC;

-- find more insight on most active user
select * from redditcomments where author = 'misdirected_asshole';

-- find more insight on most positive authors:
select * from redditcomments where author = 'HughJBawles';
select * from redditcomments where author = 'perverted_alt';

    