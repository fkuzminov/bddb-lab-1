db.products.aggregate([
    {
        $lookup: {
            from: "order_items",
            localField: "_id",
            foreignField: "product_id",
            as: "orders"
        }
    },
    { $match: { "orders": { $size: 0 } } },
    { $project: { _id: 0, name: 1 } }
]);