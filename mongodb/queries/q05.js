// Получить список категорий и количество товаров в каждой из них.

db.categories.aggregate([
    { $match: { "parent_id": { $ne: null } } },
    {
        $lookup: {
            "from": "products",
            "localField": "_id",
            "foreignField": "category_id",
            "as": "products"
        }
    },
    {
        $project: {
            "category_name": 1,
            "productCount": { $size: "$products" }
        }
    }
]);