db.orders.aggregate([
  {
    $group: {
      _id: "$customer_id",
      total_spent: { $sum: "$total_amount" }
    }
  },
  {
    $lookup: {
      from: "customers",
      localField: "_id",
      foreignField: "_id",
      as: "customer"
    }
  },
  { $unwind: "$customer" },
  // если добавишь customers.country
  {
    $setWindowFields: {
      partitionBy: "$customer.country",
      sortBy: { total_spent: -1 },
      output: { rank: { $rank: {} } }
    }
  },
  {
    $project: {
      _id: 0,
      full_name: "$customer.full_name",
      country: "$customer.country",
      total_spent: 1,
      rank: 1
    }
  }
]);
