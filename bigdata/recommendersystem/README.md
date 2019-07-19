this project produces a series of mapreduce jobs that produces a recommended ratings for each movie per user based on ItemCF algorithm. 
By creating a cocurrence matrix using the input file we will get the relations of movies (if movieA been watched by 2 person, how many people watch movieB)
the co-currency matrix helps us understand the relationship between movies, so if movieA and movieB was watched together by quite a few people
 we could indicate that these two movies are highly corrolated. Besides using the relations between movies, we also determine people's preferences 
 using the known ratings. By multipying the ratings with relations we could deduct the estimated ratings for those that have not been watched by a user.
 
input file - userId, movieId, rating
jobs -
job1 - data processing -> 
output {userId:[movie1:rating1,movie2:rating2...]}
job2 - create cooccurence matrix ->
output {movie1: movie2+relation}
job3 - normalize the cooccurence matrix (we normalize it by showing the relation using a percentage instead an actuall number since some movies might have a strong relation
which could skew the estimated ratings) ->
output {movie1: movie2+normalized_relation}
job4 - produce ratings matrix + get estimated ratings per movie per user by multiplying ratings matrix with normalized cooccurence matrix
ratings matrix input - {MovieId: userId+sub_rating}
output {movieId+userId: esimated_rating}
job5 - get estimated movie ratings for each user by summing up previous job's value 
output {movieId+UserId: rating}

