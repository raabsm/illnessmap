
db = db.getSiblingDB(dbName);

//indexes
db.Reviews.createIndex({"classification_hsan.total_score": 1});
db.Reviews.createIndex({"classification.total_score": 1});
db.Reviews.createIndex({"business_id": 1});
db.Reviews.createIndex({"classification.total_score": 1, "classification_hsan.total_score": 1});

//views

db.createView(
    "RecentSickReviews",
    "Reviews",
    [
        {
            $match: {created: {$gte: '2019-01-01'}}

        },
        {
            $match: {$or: [
                {"classification.total_score": {$gte: 0.1}},
                {"classification_hsan.total_score" : {$gte: 0.1}}
                ]
            }
        }
    ]
);


db.createView(
    "AllSickReviews",
    "Reviews",
    [{$match: {$or: [
        {"classification.total_score": {$gte: 0.1}},
                {"classification_hsan.total_score" : {$gte: 0.1}}]}}]);

db.createView( "MergedRestaurantAllReviews", "Restaurants", [ {$lookup: {  from: 'AllSickReviews', localField: '_id', foreignField: 'business_id', as: 'reviews' }}, {$match: {reviews: {$ne: []}}}] );

db.createView( "MergedRestaurantRecentReviews", "Restaurants", [ {$lookup: {  from: 'RecentSickReviews', localField: '_id', foreignField: 'business_id', as: 'reviews' }}, {$match: {reviews: {$ne: []}}}] );










