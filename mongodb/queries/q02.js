// Определить количество товаров в каждой категории.
db.categories.aggregate([
    {
        $lookup: {
            from: "products",
            localField: "_id",
            foreignField: "category_id",
            as: "products"
        }
    },
    {
        $project: {
            _id: 0,
            category_name: 1,
            product_count: { $size: "$products" }
        }
    },
    { $sort: { product_count: -1 } }
]);
