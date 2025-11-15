db.customers.aggregate([
  {
    $project: {
      full_name: 1,
      registration_month: { $month: "$registration_date" },
      registration_year: { $year: "$registration_date" }
    }
  },
  {
    $lookup: {
      from: "orders",
      localField: "_id",
      foreignField: "customer_id",
      as: "orders"
    }
  },
  {
    $group: {
      _id: { year: "$registration_year", month: "$registration_month" },
      customers: {
        $push: {
          name: "$full_name",
          orders_count: { $size: "$orders" }
        }
      }
    }
  },
  { $sort: { "_id.year": 1, "_id.month": 1 } }
]);
