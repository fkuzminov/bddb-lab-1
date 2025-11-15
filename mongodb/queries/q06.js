db.customers.aggregate([
    {
        $lookup: {
            "from": "orders",
            "localField": "_id",
            "foreignField": "customer_id",
            "as": "orders"
        }
    },
    { $match: { orders: { $eq: [] } } },
    {
        $project: {
            "_id": 0,
            "full_name": 1,
            "email": 1
        }
    }
]);