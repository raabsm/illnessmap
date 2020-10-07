
db = db.getSiblingDB(dbName);

//indexes
db.Reviews.createIndex({"classification_hsan.total_score": 1});
db.Reviews.createIndex({"classification.total_score": 1});
db.Reviews.createIndex({"business_id": 1});
db.Reviews.createIndex({"classification.total_score": 1, "classification_hsan.total_score": 1});
db.RestaurantExtraFields.createIndex({"rest_id": 1});

//views

db.createView(
    "RecentSickReviews",
    "Reviews",
    [
        {
            $match: {$or: [
                {"classification.total_score": {$gte: 0.1}},
                {"classification_hsan.total_score" : {$gte: 0.1}}
                ]
            }
        },
        {
            $match: {created: {$gte: '2019-01-01'}}

        }
    ]
);

db.createView("RestaurantsJoinExtraField",
    "Restaurants",
    [{
        $lookup: {
            from: 'RestaurantExtraFields',
            localField: '_id',
            foreignField: 'rest_id',
            as: 'doc'
        }
    }, {
        $replaceRoot: {
            newRoot: {
                $mergeObjects: [{
                        $arrayElemAt: [
                            '$doc',
                            0
                        ]
                    },
                    '$$ROOT'
                ]
            }
        }
    }, {
        $project: {
            doc: 0,
            rest_id: 0
        }
    }]
);

db.createView(
    "AllSickReviews",
    "Reviews",
    [{$match: {$or: [
        {"classification.total_score": {$gte: 0.1}},
                {"classification_hsan.total_score" : {$gte: 0.1}}]}}]);

db.createView( "MergedRestaurantAllReviews", "RestaurantsJoinExtraField", [ {$lookup: {  from: 'AllSickReviews', localField: '_id', foreignField: 'business_id', as: 'reviews' }}, {$match: {reviews: {$ne: []}}}] );

db.createView( "MergedRestaurantRecentReviews", "RestaurantsJoinExtraField", [ {$lookup: {  from: 'RecentSickReviews', localField: '_id', foreignField: 'business_id', as: 'reviews' }}, {$match: {reviews: {$ne: []}}}] );










