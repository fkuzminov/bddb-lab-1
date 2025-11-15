db.suppliers.aggregate([
    {
        $lookup: {
            from: "product_suppliers",
            localField: "_id",
            foreignField: "supplier_id",
            as: "products"
        }
    },
    {
        $project: {
            _id: 1,
            name: 1,
            product_count: { $size: "$products" }
        }
    }
]);