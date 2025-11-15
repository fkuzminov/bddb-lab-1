// Получить поставщиков и клиентов, связанных через товары, которые они
// поставляют и покупают.

db.product_suppliers.aggregate([
  {
    $lookup: {
      from: "order_items",
      localField: "product_id",
      foreignField: "product_id",
      as: "order_items"
    }
  },
  { $unwind: "$order_items" },
  {
    $lookup: {
      from: "orders",
      localField: "order_items.order_id",
      foreignField: "_id",
      as: "order"
    }
  },
  { $unwind: "$order" },
  {
    $lookup: {
      from: "customers",
      localField: "order.customer_id",
      foreignField: "_id",
      as: "customer"
    }
  },
  { $unwind: "$customer" },
  {
    $lookup: {
      from: "suppliers",
      localField: "supplier_id",
      foreignField: "_id",
      as: "supplier"
    }
  },
  { $unwind: "$supplier" },
  {
    $group: {
      _id: "$supplier.name",
      customers: { $addToSet: "$customer.full_name" }
    }
  },
  {
    $project: {
      _id: 0,
      supplier_name: "$_id",
      customers: 1
    }
  }
]);
