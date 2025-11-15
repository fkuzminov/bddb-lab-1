// Найти клиентов, сделавших самый дорогой заказ в каждой категории товаров.

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
    $lookup: {
      from: "orders",
      localField: "order_id",
      foreignField: "_id",
      as: "order"
    }
  },
  { $unwind: "$order" },
  {
    $group: {
      _id: {
        category_id: "$product.category_id",
        customer_id: "$order.customer_id"
      },
      total_spent: { $sum: { $multiply: ["$quantity", "$unit_price"] } }
    }
  },
  {
    $group: {
      _id: "$_id.category_id",
      max_spent: { $max: "$total_spent" },
      customers: {
        $push: {
          customer_id: "$_id.customer_id",
          total_spent: "$total_spent"
        }
      }
    }
  },
  {
    $project: {
      _id: 1,
      top_customers: {
        $filter: {
          input: "$customers",
          as: "cust",
          cond: { $eq: ["$$cust.total_spent", "$max_spent"] }
        }
      }
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
    $lookup: {
      from: "customers",
      localField: "top_customers.customer_id",
      foreignField: "_id",
      as: "customer"
    }
  },
  {
    $project: {
      _id: 0,
      category: "$category.category_name",
      customers: "$customer.full_name",
      spent: "$max_spent"
    }
  }
]);
