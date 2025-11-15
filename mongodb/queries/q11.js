db.order_items.aggregate([
  {
    $lookup: {
      from: "products",
      localField: "product_id",
      foreignField: "_id",
      as: "product"
    }
  },
  { $unwind: "$product" },
  {
    $group: {
      _id: "$product.category_id",
      total_sales: { $sum: { $multiply: ["$quantity", "$unit_price"] } }
    }
  },
  {
    $lookup: {
      from: "categories",
      localField: "_id",
      foreignField: "_id",
      as: "category"
    }
  },
  { $unwind: "$category" },
  {
    $project: {
      _id: 0,
      category_name: "$category.category_name",
      total_sales: { $round: ["$total_sales", 2] }
    }
  },
  { $sort: { total_sales: -1 } }
]);
