db.order_items.aggregate([
  {
    $group: {
      _id: { product_id: "$product_id", quantity: "$quantity" },
      orders: { $addToSet: "$order_id" },
      pair_count: { $sum: 1 }
    }
  },
  { $match: { pair_count: { $gt: 1 } } },
  {
    $lookup: {
      from: "products",
      localField: "_id.product_id",
      foreignField: "_id",
      as: "product"
    }
  },
  { $unwind: "$product" },
  {
    $project: {
      _id: 0,
      product_name: "$product.name",
      quantity: "$_id.quantity",
      orders: 1
    }
  }
]);