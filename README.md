# Sentimental-analysis
We worked on understanding sentimental analysis through the ACL Internet Movie Database (IMDb) dataset. The dataset consists of (50,000) reviews are paired with a label of 0 or 1 to represent negative and positive sentiment, respectively. 

These labels were linearly mapped from the IMDb’s star rating system where reviewers can rate a movie a certain number of stars from 1 to 10. The reviews with labels are split in half; each set has 12,500 positive reviews and 12,500 negative reviews to keep the data balanced

The IMDb review sentiment dataset was used for all experiments. The dataset was preprocessed to a dictionary size of 5,000 words with a zero-padded maximum sequence of 500 words per a review; anymore data became insignificant to the networks objective.  

Writing a review of maximum of 500 words, will device weather the following text is a positive feedback or negative feedback.
