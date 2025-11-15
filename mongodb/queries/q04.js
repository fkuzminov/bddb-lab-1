// Определить товары, которые поставляются более чем одним
// поставщиком.
db.products.aggregate([
    {
        $lookup: {
            "from": "product_suppliers",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "suppliers"
        }
    },
    {
        $project: {
            "name": 1,
            "supplierCount": { $size: "$suppliers" }
        }
    },
    { $match: { "supplierCount": { $gt: 1 } }}
]);