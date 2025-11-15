db.products.aggregate([
    {
        $lookup: {
            from: "categories",
            localField: "category_id",
            foreignField: "_id",
            as: "category"
        }
    },
    {
        $project: {
            _id: 1,
            name: 1,
            category: { $arrayElemAt: ["$category.category_name", 0] },
            price: 1,
            stock: 1
        }
    }
]);