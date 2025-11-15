db.order_items.aggregate([
  {
    $group: {
      _id: "$product_id",
      avg_quantity: { $avg: "$quantity" }
    }
  },
  { $match: { avg_quantity: { $lt: 2 } } }, // например, меньше 2 единиц в среднем
  {
    $lookup: {
      from: "products",
      localField: "_id",
      foreignField: "_id",
      as: "product"
    }
  },
  { $unwind: "$product" },
  {
    $project: {
      _id: 0,
      product_name: "$product.name",
      avg_quantity: { $round: ["$avg_quantity", 2] }
    }
  },
  { $sort: { avg_quantity: 1 } }
]);
